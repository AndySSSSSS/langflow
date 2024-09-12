import { useMutationFunctionType } from "@/types/api";
import { UseMutationResult } from "@tanstack/react-query";
import { AxiosResponse } from "axios";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface PostGlobalPromptParams {
  name: string;
  content: string;
  description?: string;
}

export const usePostPrompt: useMutationFunctionType<
  undefined,
  PostGlobalPromptParams
> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  const postPromptFunction = async ({
    name,
    content,
    description,
  }): Promise<AxiosResponse<{ name: string; id: string; type: string }>> => {
    const res = await api.post(`${getURL("PROMPT")}/`, {
      name,
      content,
      description,
    });
    return res.data;
  };

  const mutation: UseMutationResult<any, any, PostGlobalPromptParams> =
    mutate(["usePostPrompt"], postPromptFunction, {
      onSettled: () => {
        queryClient.refetchQueries({ queryKey: ["useGetPromptQuery"] });
      },
      ...options,
    });

  return mutation;
};
