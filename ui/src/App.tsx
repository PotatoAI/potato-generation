import React, { useState, useRef, MutableRefObject } from "react";
import {
  useAllRequestsQuery,
  useAllTasksQuery,
  useAllImagesQuery,
  useDoActionMutation,
  RequestSortEnum,
  TaskSortEnum,
  ImageSortEnum,
} from "./generated/graphql";
import { DataGrid, GridColDef } from "@mui/x-data-grid";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Portal from "@mui/material/Portal";

import RefreshIcon from "@mui/icons-material/Refresh";

import { LoadingModal } from "./Loading";
import { ImageViewer } from "./ImageViewer";
import { Submit } from "./Submit";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

const RefreshButton = (props: { refresh: () => void }) => {
  return (
    <IconButton onClick={props.refresh}>
      <RefreshIcon />
    </IconButton>
  );
};

const AppTabs = (props: {
  currentTab: number;
  changeTab: (tab: number) => void;
  allTabs: Array<string>;
}) => {
  const { currentTab, changeTab, allTabs } = props;

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    changeTab(newValue);
  };

  return (
    <Tabs
      value={currentTab}
      onChange={handleChange}
      aria-label="basic tabs example"
    >
      {allTabs.map((tab, i) => (
        <Tab label={tab} {...a11yProps(i)} key={tab} />
      ))}
    </Tabs>
  );
};

const dateColW = 150;
const gridSX = { height: "calc(100vh - 70px)", width: "100%" };

const RequestsDataGrid = (props: { portalRef: MutableRefObject<null> }) => {
  const [selected, setSelected] = useState<Array<string>>([]);
  const [result, refresh] = useAllRequestsQuery({
    variables: { sort: RequestSortEnum.CreatedOnDesc },
    requestPolicy: "network-only",
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "prompt",
      width: 250,
    },
    { field: "approved", width: 90 },
    { field: "generated", width: 90 },
    { field: "kind" },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    {
      field: "images",
      renderCell: (p) => {
        const oids = p.row.images.edges.map(
          (i: { node: { oid: number } }) => i.node.oid
        );
        return <ImageViewer oids={oids} />;
      },
    },
    {
      field: "tasks",
      valueGetter: (params) => params.row.tasks["edges"].length,
    },
  ];

  const rows = data?.allRequests?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const approveSelected = async () => {
    await action({ ids: selected, action: "approve", model: "request" });
    await refresh({ requestPolicy: "network-only" });
  };

  const deleteSelected = async () => {
    await action({ ids: selected, action: "delete", model: "request" });
    await refresh({ requestPolicy: "network-only" });
  };

  const reRunSelected = async () => {
    await action({ ids: selected, action: "re-run", model: "request" });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={30}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
        onSelectionModelChange={(ids) => setSelected(ids as string[])}
      />
    </Box>
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching} />
      {dataGrid}
      <Portal container={props.portalRef.current}>
        <Button
          disabled={selected.length === 0}
          onClick={approveSelected}
          color="success"
        >
          Approve
        </Button>
        <Button
          disabled={selected.length === 0}
          onClick={deleteSelected}
          color="error"
        >
          Delete
        </Button>
        <Button
          disabled={selected.length === 0}
          onClick={reRunSelected}
          color="warning"
        >
          Re-Run
        </Button>
        <RefreshButton
          refresh={() => refresh({ requestPolicy: "network-only" })}
        />
      </Portal>
    </>
  );
};

const TasksDataGrid = (props: { portalRef: MutableRefObject<null> }) => {
  const [selected, setSelected] = useState<Array<string>>([]);
  const [result, refresh] = useAllTasksQuery({
    variables: { sort: TaskSortEnum.CreatedOnDesc },
    requestPolicy: "network-only",
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    { field: "running" },
    { field: "status" },
    {
      field: "error",
      width: 150,
    },
    {
      field: "log",
      width: 150,
    },
    { field: "priority" },
    { field: "workerId", width: 120 },
    { field: "kind" },
    {
      field: "images",
      renderCell: (p) => {
        const oids = p.row.images.edges.map(
          (i: { node: { oid: number } }) => i.node.oid
        );
        return <ImageViewer oids={oids} />;
      },
    },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
  ];

  const rows = data?.allTasks?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const deleteSelected = async () => {
    await action({ ids: selected, action: "delete", model: "task" });
    await refresh({ requestPolicy: "network-only" });
  };

  const reRunSelected = async () => {
    await action({ ids: selected, action: "re-run", model: "task" });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={30}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
        onSelectionModelChange={(ids) => setSelected(ids as string[])}
      />
    </Box>
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching} />
      {dataGrid}
      <Portal container={props.portalRef.current}>
        <Button
          disabled={selected.length === 0}
          onClick={deleteSelected}
          color="error"
        >
          Delete
        </Button>
        <Button
          disabled={selected.length === 0}
          onClick={reRunSelected}
          color="warning"
        >
          Re-Run
        </Button>
        <RefreshButton
          refresh={() => refresh({ requestPolicy: "network-only" })}
        />
      </Portal>
    </>
  );
};

const ImagesDataGrid = (props: { portalRef: MutableRefObject<null> }) => {
  const [selected, setSelected] = useState<Array<string>>([]);
  const [result, refresh] = useAllImagesQuery({
    variables: { sort: ImageSortEnum.CreatedOnDesc },
    requestPolicy: "network-only",
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "oid",
      renderCell: (p) => {
        return <ImageViewer oids={[p.row.oid]} />;
      },
    },
    { field: "filename" },
    { field: "selected" },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
    { field: "taskId" },
  ];

  const rows = data?.allImages?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const selectSelected = async () => {
    await action({ ids: selected, action: "select", model: "image" });
    await refresh({ requestPolicy: "network-only" });
  };

  const deleteSelected = async () => {
    await action({ ids: selected, action: "delete", model: "image" });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={30}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
        onSelectionModelChange={(ids) => setSelected(ids as string[])}
      />
    </Box>
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching} />
      {dataGrid}
      <Portal container={props.portalRef.current}>
        <Button
          disabled={selected.length === 0}
          onClick={selectSelected}
          color="success"
        >
          Select
        </Button>
        <Button
          disabled={selected.length === 0}
          onClick={deleteSelected}
          color="error"
        >
          Delete
        </Button>
        <RefreshButton
          refresh={() => refresh({ requestPolicy: "network-only" })}
        />
      </Portal>
    </>
  );
};

const App = () => {
  const allTabs = ["requests", "tasks", "images"];
  const [currentTabI, setCurrentTabI] = useState(0);
  const currentTab = allTabs[currentTabI];
  const container = useRef(null);

  // const [res] = useChangeNotificationSubscription();
  // console.log(res);

  let dataGrid = <RequestsDataGrid portalRef={container} />;

  if (currentTab === "tasks") {
    dataGrid = <TasksDataGrid portalRef={container} />;
  }

  if (currentTab === "images") {
    dataGrid = <ImagesDataGrid portalRef={container} />;
  }

  return (
    <Box>
      <Box
        sx={{
          borderBottom: 1,
          borderColor: "divider",
          justifyContent: "space-between",
          flexDirection: "row",
          display: "flex",
        }}
      >
        <AppTabs
          currentTab={currentTabI}
          changeTab={setCurrentTabI}
          allTabs={allTabs}
        />
        <Box
          sx={{ margin: "auto 15px", display: "flex", flexDirection: "row" }}
        >
          <Submit />
        </Box>
        <Box sx={{ margin: "auto 15px" }} ref={container}></Box>
      </Box>
      {dataGrid}
    </Box>
  );
};

export default App;
