import Loading from "@/components/ui/loading";
import {
  useDeletePrompt,
  usePatchPrompt,
} from "@/controllers/API/queries/prompt";
import { useIsFetching } from "@tanstack/react-query";
import {
  NewValueParams,
  SelectionChangedEvent,
} from "ag-grid-community";
import cloneDeep from "lodash/cloneDeep";
import {useEffect, useState} from "react";
import TableComponent from "@/components/tableComponent";
import useAlertStore from "@/stores/alertStore";
import { usePromptStore } from "@/stores/promptStore";
import TableAutoCellRender from "@/components/tableComponent/components/tableAutoCellRender";

const COLUMNS = [{
  field: 'name',
  headerName: '名称',
  flex: 1
}, {
  field: 'content',
  headerName: '内容',
  flex: 1
}, {
  field: 'description',
  headerName: '备注',
  flex: 1
}, {
  field: 'created_at',
  headerName: '创建时间',
  flex: 1
}]

export default function PromptView() {
  const columns = usePromptStore((state) => state.columns);
  const promptList = usePromptStore((state) => state.promptList);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const updatePrompt = usePromptStore((state) => state.updatePrompt);
  const deletePromptStore = usePromptStore((state) => state.removePromptByIds);
  const isFetching = useIsFetching({
    queryKey: ["useGetPromptQuery"],
    exact: false,
  });
  const [selectedRows, setSelectedRows] = useState<string[]>([]);

  const { mutate: deletePromptList } = useDeletePrompt({
    onSuccess: () => {
      deletePromptStore(selectedRows);
      setSelectedRows([]);
      setSuccessData({
        title: "Prompt deleted successfully.",
      });
    },
    onError: () => {
      setErrorData({
        title: "Error deleting prompt.",
      });
    },
  });

  const { mutate: updatePromptMutation } = usePatchPrompt();

  function handleUpdatePrompt(event: NewValueParams<any, string>) {
    const newValue = event.newValue;
    const field = event.column.getColId();
    const row = cloneDeep(event.data);
    const data = {
      ...row,
      [field]: newValue,
    };
    updatePromptMutation(data, {
      onSuccess: () => {
        updatePrompt(data);
        // Set success message
        setSuccessData({
          title: "修改成功！",
        });
      },
      onError: (error) => {
        const msg = error?.response?.data?.detail
        setErrorData({
          title: (typeof msg === 'string' && msg) || "修改失败，请重试！",
        });
        event.data[field] = event.oldValue;
        event.api.refreshCells();
      },
    });
  }

  function handleRemovePrompt() {
    deletePromptList({ ids: selectedRows });
  }

  useEffect(() => {
    const _columns = COLUMNS.map(v => ({
      ...v,
      filter: true,
      cellRenderer: TableAutoCellRender,
      resizable: true,
      tooltipField: v.field,
    }));

    usePromptStore.getState().setColumns(_columns)
  }, []);

  return isFetching > 0 ? (
    <div className="flex h-full w-full items-center justify-center align-middle">
      <Loading></Loading>
    </div>
  ) : (
    <TableComponent
      key={"PromptView"}
      onDelete={handleRemovePrompt}
      readOnlyEdit
      editable={[
        { field: "name", onUpdate: handleUpdatePrompt, editableCell: false },
        { field: "description", onUpdate: handleUpdatePrompt, editableCell: false },
        { field: "content", onUpdate: handleUpdatePrompt, editableCell: false },
      ]}
      overlayNoRowsTemplate="No data available"
      onSelectionChanged={(event: SelectionChangedEvent) => {
        setSelectedRows(event.api.getSelectedRows().map((row) => row.id));
      }}
      rowSelection="multiple"
      suppressRowClickSelection={true}
      pagination={true}
      columnDefs={columns}
      rowData={promptList}
    />
  );
}