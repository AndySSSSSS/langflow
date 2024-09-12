import { useMutationFunctionType } from "@/types/api";
import { UseMutationResult } from "@tanstack/react-query";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface DeletePromptParams {
  ids: string[];
}

export const useDeletePrompt: useMutationFunctionType<
  undefined,
  DeletePromptParams
> = (options?) => {
  const { mutate } = UseRequestProcessor();

  const deletePrompt = async ({ ids }: DeletePromptParams): Promise<any> => {
    const response = await api.delete(`${getURL("PROMPT")}`, {
      data: ids,
    });

    return response.data;
  };

  const mutation: UseMutationResult<
    DeletePromptParams,
    any,
    DeletePromptParams
  > = mutate(["useDeletePrompt"], deletePrompt, options);

  return mutation;
};
