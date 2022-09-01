import React, { useState, useRef, MutableRefObject } from "react";
import {
  useAllRequestsQuery,
  useAllTasksQuery,
  useAllImagesQuery,
  useRequestsActionMutation,
  RequestSortEnum,
  TaskSortEnum,
  ImageSortEnum,
} from "./generated/graphql";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { ChaoticOrbit } from "@uiball/loaders";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Portal from '@mui/material/Portal';

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

const loader = (
  <Box justifyContent="center" height="100vh" width="100%">
    <ChaoticOrbit size={25} speed={1.5} color="white" />
  </Box>
);

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
    <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
      <Tabs
        value={currentTab}
        onChange={handleChange}
        aria-label="basic tabs example"
      >
        {allTabs.map((tab, i) => (
          <Tab label={tab} {...a11yProps(i)} key={tab} />
        ))}
      </Tabs>
    </Box>
  );
};

const dateColW = 150;
const gridSX = { height: "calc(100vh - 70px)", width: "100%" };

const RequestsDataGrid = (props: {portalRef: MutableRefObject<null>}) => {
  const [selected, setSelected] = useState<Array<string>>([]);
  const [result, refresh] = useAllRequestsQuery({
    variables: { sort: RequestSortEnum.CreatedOnDesc },
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
      field: "tasks",
      valueGetter: (params) => params.row.tasks["edges"].length,
    },
    {
      field: "images",
      valueGetter: (params) => params.row.images["edges"].length,
    },
  ];

  const rows = data?.allRequests?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useRequestsActionMutation();

  const approveSelected = async () => {
    await action({ids: selected, action: "approve"});
    await refresh({ requestPolicy: 'network-only' });
  }

  const deleteSelected = async () => {
    await action({ids: selected, action: "delete"});
    await refresh({ requestPolicy: 'network-only' });
  }

  const reRunSelected = async () => {
    await action({ids: selected, action: "re-run"});
    await refresh({ requestPolicy: 'network-only' });
  }

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
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
      {fetching ? loader : dataGrid}
      <Portal container={props.portalRef.current}>
        <Button disabled={selected.length === 0} onClick={approveSelected}>Approve</Button>
        <Button disabled={selected.length === 0} onClick={deleteSelected}>Delete</Button>
        <Button disabled={selected.length === 0} onClick={reRunSelected}>Re-Run</Button>
      </Portal>
    </>
  );
};

const TasksDataGrid = (props: {portalRef: MutableRefObject<null>}) => {
  const [result] = useAllTasksQuery({
    variables: { sort: TaskSortEnum.CreatedOnDesc },
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    { field: "running" },
    { field: "status" },
    {
      field: "error",
      width: 250,
    },
    { field: "priority" },
    { field: "workerId", width: 120 },
    { field: "kind" },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
  ];

  const rows = data?.allTasks?.edges?.map((edge) => edge?.node) ?? [];

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
      />
    </Box>
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      {fetching ? loader : dataGrid}
    </>
  );
};

const ImagesDataGrid = (props: {portalRef: MutableRefObject<null>}) => {
  const [result] = useAllImagesQuery({
    variables: { sort: ImageSortEnum.CreatedOnDesc },
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    { field: "filename" },
    { field: "selected" },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
    { field: "taskId" },
  ];

  const rows = data?.allImages?.edges?.map((edge) => edge?.node) ?? [];

  const dataGrid = (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
      />
    </Box>
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      {fetching ? loader : dataGrid}
    </>
  );
};

const App = () => {
  const allTabs = ["requests", "tasks", "images"];
  const [currentTabI, setCurrentTabI] = useState(0);
  const currentTab = allTabs[currentTabI];
  const container = useRef(null)

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
      <AppTabs
        currentTab={currentTabI}
        changeTab={setCurrentTabI}
        allTabs={allTabs}
      />
      <Box ref={container}></Box>
      {dataGrid}
    </Box>
  );
};

export default App;
