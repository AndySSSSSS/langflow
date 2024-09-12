import { useGetPromptQuery } from "@/controllers/API/queries/prompt";
import PromptView from "./components/PromptView";
import HeaderPromptComponent from "./components/headerPrompt";

export default function PromptPage() {
  useGetPromptQuery({});

  return (
    <div className="flex h-full w-full flex-col justify-between gap-6">
      <HeaderPromptComponent />
      <div className="flex h-full w-full flex-col justify-between">
        <PromptView />
      </div>
    </div>
  );
}
