import ForwardedIconComponent from "../../../../../../components/genericIconComponent";
import AddNewPromptButton from "../addNewPromptButton";
import {Button} from "@/components/ui/button";
import IconComponent from "@/components/genericIconComponent";

const HeaderPromptComponent = () => {
  return (
    <>
      <div className="flex w-full items-center justify-between gap-4 space-y-0.5">
        <div className="flex flex-col">
          <h2 className="flex items-center text-lg font-semibold tracking-tight">
            Prompt
            <ForwardedIconComponent
                name="TerminalSquare"
                className="ml-2 h-5 w-5 text-primary"
            />
          </h2>
          {/*<p className="text-sm text-muted-foreground">*/}
          {/*  Inspect, edit and remove messages to explore and refine model*/}
          {/*  behaviors.*/}
          {/*</p>*/}
        </div>
        <div className="flex flex-shrink-0 items-center gap-2">
          <AddNewPromptButton asChild>
            <Button data-testid="api-key-button-store" variant="primary">
              <IconComponent name="Plus" className="w-4"/>
              Add New
            </Button>
          </AddNewPromptButton>
        </div>
      </div>
    </>
  );
};
export default HeaderPromptComponent;
