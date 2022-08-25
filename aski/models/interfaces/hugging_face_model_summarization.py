""" 
====================================================
Hugging Face Model Summary 
====================================================
This module extends the ModelSummary interface to load Hugging Face models.

"""

from os.path import exists
import nltk
from nltk import sent_tokenize
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, SummarizationPipeline
from transformers.pipelines.base import KeyDataset

from aski.models.interfaces.model_summarization import ModelSummarization

# generate chunks of text \ sentences <= 1024 tokens
def nest_sentences(document):
    print(type(document))
    nltk.download('punkt')
    nested = []
    sent = []
    length = 0
    for sentence in sent_tokenize(document):
        length += len(sentence)
    if length < 1024:
        sent.append(sentence)
    else:
        nested.append(sent)
        sent = []
        length = 0

    if sent:
        nested.append(sent)
    return nested

class HuggingFaceModelSummarization(ModelSummarization):
    """
    A Superclass used to build HuggingFace models for summarization


    Attributes
    ----------
    _info : dictionnary
        A dictionnary containing the name, class name, description, paper link 
        and GitHub repo link of the model
    _max_length : int
        The maximum length parameter of the model
    _truncation : boolean
        Whether or not to truncate input sequences
    _model : AutoModelForSeq2SeqLM
        A HuggingFace model for summarization
    _tokenizer : AutoTokenizer
        A HuggingFace tokenizer 
    _pipe : SummarizationPipeline
        A HuggingFace pipeline for summarization

    Methods
    -------
    _summarize_dataset(self, dataset, column):
        Summarizes a dataset and appends to it a column with the summarized text.

    _summarize_text(self, text_to_summarize):
        Summarizes a piece of text and returns it.

    """

    def __init__(self, model_name, max_length, model_max_length, truncation, model_info, verbose=True):

        self._info       = model_info
        self._max_length = max_length
        self._truncation = truncation

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' model...')

        self._model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, 
            max_length=max_length)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' tokenizer...')

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            max_length=max_length,
            model_max_length=model_max_length,
            truncation=truncation)

        if verbose == True:
            print('> Loading ' + self._info['name'] + ' pipe...')

        self._pipe = SummarizationPipeline(
            model=self._model, 
            tokenizer=self._tokenizer)

        if verbose == True:

            print('\n> Finished loading ' + self._info['name'] + ' class.\n')

    def _summarize_dataset(self, dataset):
        """ 
        Method that takes in a HuggingFace dataset and the name of the column of
        the dataset that contains the text to summarize. It calls the 
        summarization pipeline attribute and runs it on the whole dataset. It 
        saves the results in a list and adds this list to the dataset object and
        returns it.

        Parameters
        ----------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize
        column : str
            The name of the column ofthe dataset with the text to summarize

        Returns
        -------
        dataset : a HuggingFace dataset object
            The HuggingFace dataset to summarize with the summarized text column
        """

        # Path where the summarization results are stored
        results_file_path = 'aski/results/' + self._info['name'] + '_' + dataset._dataset_name + '.csv'

        # To store the summarization results (will later be added to the dataset)
        summarization_outputs = []

        # If we already ran the model for this dataset, read the saved results
        if exists(results_file_path):

            # Read the first column of the csv file which contains the summaries
            df = pd.read_csv(results_file_path)
            summarization_outputs = df[df.columns[0]]

            # Add the column to the dataset object to be able to compute metrics
            dataset._dataset[dataset._split] = dataset._dataset[dataset._split].add_column(
                name=('result_' + self._info['class_name']), 
                column=summarization_outputs)
        else:
            for output in tqdm(self._pipe(KeyDataset(dataset._dataset[dataset._split], dataset._document_column))):

                answer = output[0]['summary_text']
                summarization_outputs.append(answer)

            # Save the results to a pandas dataframe and dump it to csv
            df = pd.DataFrame(summarization_outputs)
            df.to_csv(results_file_path, index=False)

            # Add the column to the dataset object to be able to compute metrics
            dataset._dataset[dataset._split] = dataset._dataset[dataset._split].add_column(
                name=('result' + self._info['class_name']), 
                column=summarization_outputs)

        return dataset

    def _summarize_text(self, document):
        """ 
        Method that takes in a piece of text and summarizes it by calling the 
        tokenizer and model attributes and finally returns it.

        Parameters
        ----------
        document : str
            The document to summarize

        Returns
        -------
        summary : List of str
            The summarized text as a list of strings
        """

        inputs_no_trunc = self._tokenizer(document, max_length=None, return_tensors='pt', truncation=False)

        chunk_start = 0
        chunk_end   = self._tokenizer.model_max_length  
        inputs_batch_lst = []

        while chunk_start <= len(inputs_no_trunc['input_ids'][0]):

            inputs_batch  = inputs_no_trunc['input_ids'][0][chunk_start:chunk_end]  
            inputs_batch  = torch.unsqueeze(inputs_batch, 0)
            chunk_start  += self._tokenizer.model_max_length  
            chunk_end    += self._tokenizer.model_max_length  
            inputs_batch_lst.append(inputs_batch)

        summary_ids_lst = [self._model.generate(inputs, num_beams=4, min_length=30, max_length=50) for inputs in inputs_batch_lst]

        summary_batch_lst = []

        for summary_id in summary_ids_lst:

            summary_batch = [self._tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_id]
            summary_batch_lst.append(summary_batch[0])

        summary_all = '\n'.join(summary_batch_lst)

        return summary_all
















