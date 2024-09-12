import {
  usePostPrompt,
} from "@/controllers/API/queries/prompt";
import { useState } from "react";
import BaseModal from "@/modals/baseModal";
import useAlertStore from "@/stores/alertStore";
import { ResponseErrorDetailAPI } from "@/types/api";
import ForwardedIconComponent from "@/components/genericIconComponent";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function AddNewPromptButton({
  children,
  asChild,
}: {
  children: JSX.Element;
  asChild?: boolean;
}): JSX.Element {
  const [key, setKey] = useState("");
  const [content, setContent] = useState("");
  const [description, setDescription] = useState("");
  const [open, setOpen] = useState(false);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const { mutate: mutateAddGlobalVariable } = usePostPrompt();

  const setSuccessData = useAlertStore((state) => state.setSuccessData);

  function handleSavePrompt() {
    let data: {
      name: string;
      content: string;
      description?: string;
    } = {
      name: key,
      description,
      content,
    };

    mutateAddGlobalVariable(data, {
      onSuccess: (res) => {
        setKey("");
        setContent("");
        setDescription("");
        setOpen(false);

        setSuccessData({
          title: `创建成功！`,
        });
      },
      onError: (error) => {
        let responseError = error as ResponseErrorDetailAPI;
        setErrorData({
          title: "提示",
          list: [
            responseError?.response?.data?.detail ??
              "prompt创建失败，请重试。",
          ],
        });
      },
    });
  }

  return (
    <BaseModal
      open={open}
      setOpen={setOpen}
      size="x-small"
      onSubmit={handleSavePrompt}
    >
      <BaseModal.Header
        description=""
      >
        <span className="pr-2"> Prompt </span>
        <ForwardedIconComponent
          name="TerminalSquare"
          className="h-6 w-6 pl-1 text-primary"
          aria-hidden="true"
        />
      </BaseModal.Header>
      <BaseModal.Trigger asChild={asChild}>{children}</BaseModal.Trigger>
      <BaseModal.Content>
        <div className="flex h-full w-full flex-col gap-4 align-middle">
          <Label>名称</Label>
          <Input
            value={key}
            onChange={(e) => {
              setKey(e.target.value);
            }}
            placeholder="请输入名称"
          ></Input>
          <Label>内容</Label>
          <Textarea
            value={content}
            onChange={(e) => {
              setContent(e.target.value);
            }}
            placeholder="请输入内容"
            className="w-full h-[200px] resize-none custom-scroll"
          />
          <Label>备注</Label>
          <Textarea
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
            }}
            placeholder="请输入备注"
            className="w-full h-[100px] resize-none custom-scroll"
          />
        </div>
      </BaseModal.Content>
      <BaseModal.Footer
        submit={{ label: "Save", dataTestId: "save-prompt-btn" }}
      />
    </BaseModal>
  );
}
