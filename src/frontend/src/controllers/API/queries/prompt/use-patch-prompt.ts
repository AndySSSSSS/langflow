import { useMutationFunctionType } from "@/types/api";
import { UseMutationResult } from "@tanstack/react-query";
import { api } from "../../api";
import { getURL } from "../../helpers/constants";
import { UseRequestProcessor } from "../../services/request-processor";

interface PatchPromptParams {
  name: string;
  content: string;
  description?: string;
  id: string;
}

export const usePatchPrompt: useMutationFunctionType<
  undefined,
  PatchPromptParams
> = (options?) => {
  const { mutate, queryClient } = UseRequestProcessor();

  async function patchPrompt({
    name,
    content,
    description,
    id,
  }: PatchPromptParams): Promise<any> {
    const res = await api.patch(`${getURL("PROMPT")}/${id}`, {
      name,
      content,
      description,
    });
    return res.data;
  }

  const mutation: UseMutationResult<
    PatchPromptParams,
    any,
    PatchPromptParams
  > = mutate(["usePatchPrompt"], patchPrompt, {
    onSettled: () => {
      queryClient.refetchQueries({ queryKey: ["useGetPromptQuery"] });
    },
    ...options,
  });

  return mutation;
};
