import { ColDef, ColGroupDef } from "ag-grid-community";
import { Prompt } from "../../prompt";

export type PromptStoreType = {
  promptList: Prompt[];
  setPromptList: (messages: Prompt[]) => void;
  addPrompt: (message: Prompt) => void;
  removePrompt: (message: Prompt) => void;
  updatePrompt: (message: Prompt) => void;
  clearPromptList: () => void;
  removePromptByIds: (ids: string[]) => void;
  columns: Array<ColDef | ColGroupDef>;
  setColumns: (columns: Array<ColDef | ColGroupDef>) => void;
  deleteSession: (id: string) => void;
};
