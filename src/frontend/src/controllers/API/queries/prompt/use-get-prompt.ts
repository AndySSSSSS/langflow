import {usePromptStore} from "@/stores/promptStore";
import {keepPreviousData} from "@tanstack/react-query";
import {ColDef, ColGroupDef} from "ag-grid-community";
import {useQueryFunctionType} from "@/types/api";
import {api} from "../../api";
import {getURL} from "../../helpers/constants";
import {UseRequestProcessor} from "../../services/request-processor";

interface PromptQueryParams {
  id?: string;
  excludedFields?: string[];
  params?: object;
}

interface PromptResponse {
  rows: Array<object>;
  columns: Array<ColDef | ColGroupDef>;
}

export const useGetPromptQuery: useQueryFunctionType<
  PromptQueryParams,
  PromptResponse
> = ({ id, params }, options) => {
  const { query } = UseRequestProcessor();

  const getPromptFn = async (id?: string, params = {}) => {
    const config = {};
    if (params) {
      config["params"] = { ...config["params"], ...params };
    }
    return await api.get<any>(`${getURL("PROMPT")}`, config);
  };

  const responseFn = async () => {
    const data = await getPromptFn(id, params);
    usePromptStore.getState().setPromptList(data.data);
    return { rows: data };
  };

  return query(["useGetPromptQuery", {id}], responseFn, {
    placeholderData: keepPreviousData,
    ...options,
  });
};
