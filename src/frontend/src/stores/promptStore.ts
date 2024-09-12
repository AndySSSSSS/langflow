import { create } from "zustand";
import { PromptStoreType } from "../types/zustand/prompt";

export const usePromptStore = create<PromptStoreType>((set, get) => ({
  deleteSession: (id) => {
    set((state) => {
      const updatedPromptList = state.promptList.filter(
        (msg) => msg.session_id !== id,
      );
      return { promptList: updatedPromptList };
    });
  },
  columns: [],
  setColumns: (columns) => {
    set(() => ({ columns: columns }));
  },
  promptList: [],
  setPromptList: (promptList) => {
    set(() => ({ promptList }));
  },
  addPrompt: (prompt) => {
    set(() => ({ promptList: [...get().promptList, prompt] }));
  },
  removePrompt: (prompt) => {
    set(() => ({
      promptList: get().promptList.filter((p) => p.id !== prompt.id),
    }));
  },
  updatePrompt: (prompt) => {
    set(() => ({
      promptList: get().promptList.map((p) =>
        p.id === prompt.id ? prompt : p,
      ),
    }));
  },
  clearPromptList: () => {
    set(() => ({ promptList: [] }));
  },
  removePromptByIds: (ids) => {
    return new Promise((resolve, reject) => {
      try {
        set((state) => {
          const updatedPromptList = state.promptList.filter(
            (prompt) => !ids.includes(prompt.id),
          );
          get().setPromptList(updatedPromptList);
          resolve(updatedPromptList);
          return { promptList: updatedPromptList };
        });
      } catch (error) {
        reject(error);
      }
    });
  },
}));
