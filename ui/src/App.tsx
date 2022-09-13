import React, { useState, useRef, MutableRefObject } from "react";
import {
  useAllRequestsQuery,
  useAllTasksQuery,
  useAllImagesQuery,
  useAllVideosQuery,
  useDoActionMutation,
  RequestSortEnum,
  TaskSortEnum,
  ImageSortEnum,
  VideoSortEnum,
} from "./generated/graphql";
import { DataGrid, GridColDef, GridRowId } from "@mui/x-data-grid";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Portal from "@mui/material/Portal";

import RefreshIcon from "@mui/icons-material/Refresh";

import { LoadingModal } from "./Loading";
import { MediaViewer } from "./MediaViewer";
import { Submit } from "./Submit";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function MyDataGrid<T>(props: {
  rows: Array<T>;
  columns: GridColDef[];
  onSelectionModelChange: (ids: GridRowId[]) => void;
}) {
  const gridSX = { height: "calc(100vh - 70px)", width: "100%" };
  const { rows, columns, onSelectionModelChange } = props;

  return (
    <Box sx={gridSX}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={30}
        rowsPerPageOptions={[5]}
        checkboxSelection
        disableSelectionOnClick
        onSelectionModelChange={onSelectionModelChange}
      />
    </Box>
  );
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
    {
      field: "images",
      renderCell: (p) => {
        const data = p.row.images.edges.map(
          (i: { node: { oid: number; id: number } }) => i.node
        );
        return <MediaViewer mediaData={data} kind="image" />;
      },
    },
    {
      field: "videos",
      renderCell: (p) => {
        const data = p.row.videos.edges.map(
          (i: { node: { oid: number; id: number } }) => i.node
        );
        return <MediaViewer mediaData={data} kind="video" />;
      },
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
  ];

  const rows = data?.allRequests?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const approveSelected = async () => {
    await action({
      ids: selected,
      action: "approve",
      model: "request",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const deleteSelected = async () => {
    await action({
      ids: selected,
      action: "delete",
      model: "request",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const reRunSelected = async () => {
    const count = prompt("How many times?") ?? "1";
    await action({
      ids: selected,
      action: "re-run",
      model: "request",
      metadata: [count],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const copySelected = async () => {
    const count = prompt("How many times?") ?? "5";
    await action({
      ids: selected,
      action: "copy",
      model: "request",
      metadata: [count],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const upscaleSelected = async () => {
    await action({
      ids: selected,
      action: "upscale",
      model: "request",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const genVid = async () => {
    await action({
      ids: selected,
      action: "generate-video",
      model: "request",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <MyDataGrid
      rows={rows}
      columns={columns}
      onSelectionModelChange={(ids) => setSelected(ids as string[])}
    />
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching || actionResult.fetching} />
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
          onClick={genVid}
          color="success"
        >
          make video
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
        <Button
          disabled={selected.length === 0}
          onClick={upscaleSelected}
          color="warning"
        >
          Upscale
        </Button>
        <Button
          disabled={selected.length === 0}
          onClick={copySelected}
          color="warning"
        >
          Copy
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
        const data = p.row.images.edges.map(
          (i: { node: { oid: number; id: string } }) => i.node
        );
        return <MediaViewer mediaData={data} kind="image" />;
      },
    },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
  ];

  const rows = data?.allTasks?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const deleteSelected = async () => {
    await action({
      ids: selected,
      action: "delete",
      model: "task",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const reRunSelected = async () => {
    await action({
      ids: selected,
      action: "re-run",
      model: "task",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <MyDataGrid
      rows={rows}
      columns={columns}
      onSelectionModelChange={(ids) => setSelected(ids as string[])}
    />
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching || actionResult.fetching} />
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
        return <MediaViewer mediaData={[p.row]} kind="image" />;
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
    await action({
      ids: selected,
      action: "select",
      model: "image",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const deleteSelected = async () => {
    await action({
      ids: selected,
      action: "delete",
      model: "image",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <MyDataGrid
      rows={rows}
      columns={columns}
      onSelectionModelChange={(ids) => setSelected(ids as string[])}
    />
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching || actionResult.fetching} />
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

const VideosDataGrid = (props: { portalRef: MutableRefObject<null> }) => {
  const [selected, setSelected] = useState<Array<string>>([]);
  const [result, refresh] = useAllVideosQuery({
    variables: { sort: VideoSortEnum.CreatedOnDesc },
    requestPolicy: "network-only",
  });

  const { data, fetching, error } = result;

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "oid",
      renderCell: (p) => {
        return <MediaViewer mediaData={[p.row]} kind="video" />;
      },
    },
    { field: "filename" },
    { field: "selected" },
    { field: "createdOn", width: dateColW },
    { field: "updatedOn", width: dateColW },
    { field: "requestId" },
    { field: "taskId" },
  ];

  const rows = data?.allVideos?.edges?.map((edge) => edge?.node) ?? [];

  const [actionResult, action] = useDoActionMutation();

  const selectSelected = async () => {
    await action({
      ids: selected,
      action: "select",
      model: "video",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const deleteSelected = async () => {
    await action({
      ids: selected,
      action: "delete",
      model: "video",
      metadata: [],
    });
    await refresh({ requestPolicy: "network-only" });
  };

  const dataGrid = (
    <DataGrid
      rows={rows}
      columns={columns}
      onSelectionModelChange={(ids) => setSelected(ids as string[])}
    />
  );

  return (
    <>
      <p>{error ? JSON.stringify(error) : ""}</p>
      <LoadingModal loading={fetching || actionResult.fetching} />
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
  const allTabs = ["requests", "tasks", "images", "videos"];
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

  if (currentTab === "videos") {
    dataGrid = <VideosDataGrid portalRef={container} />;
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
