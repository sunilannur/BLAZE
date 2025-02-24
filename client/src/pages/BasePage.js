import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

import { setConfig } from "../slice/configLoadSlice";

import { SearchPage } from "./search/Search";
import { SummarizationPage } from "./summarization/Summarization";


export function BasePage() {
  const dispatch = useDispatch();
  React.useEffect(() => {
    dispatch(setConfig());
  }, []);
  const config = useSelector((state) => state.config.config);

  if (config == null) {
    return <></>;
  }

  if (config["function"]["task"]==="search") {
   return <SearchPage config={config}/> 
  }

  if (config["function"]["task"]==="summarization") {
    return <SummarizationPage config={config}/> 
   }


 

}
