import React, { useState } from "react";
import {
  useDoActionMutation,
  useInputFilesQuery,
  useImagesByIdQuery,
} from "./generated/graphql";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import PlayCircleIcon from "@mui/icons-material/PlayCircle";
import { ChaoticOrbit } from "@uiball/loaders";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
};

interface MediaData {
  id: string;
  oid: number;
}

type Props = {
  mediaData: Array<MediaData>;
  kind: "video" | "image";
};

const ExtraControlsVideo = (props: { id: string }) => {
  const { id } = props;
  const [actionResult, action] = useDoActionMutation();
  const [inputFiles, refreshInputFiles] = useInputFilesQuery({
    requestPolicy: "network-only",
  });
  const [selectedFile, setSelectedFile] = useState("");

  const select = async () => {
    await action({
      ids: [id],
      action: "add-audio",
      model: "video",
      metadata: [selectedFile],
    });
  };

  const loader = <ChaoticOrbit size={25} speed={1.5} color="white" />;

  return (
    <Box>
      {inputFiles.fetching ? (
        loader
      ) : (
        <Select
          value={selectedFile}
          onChange={(e) => setSelectedFile(e.target.value)}
        >
          {inputFiles?.data?.inputFiles?.map((f) => {
            if (f) {
              return (
                <MenuItem value={f} key={f}>
                  {f.slice(-25)}
                </MenuItem>
              );
            }
          })}
        </Select>
      )}
      <Button onClick={select}>
        {actionResult.fetching ? loader : "Add audio"}
      </Button>
    </Box>
  );
};

const ExtraControlsImage = (props: { id: string }) => {
  const { id } = props;
  const [actionResult, action] = useDoActionMutation();
  const [imageDetails, refresh] = useImagesByIdQuery({
    variables: { imageIds: [id] },
    requestPolicy: "network-only",
  });

  const isSelected = imageDetails.data?.imagesById?.some(
    (img) => img?.selected
  );

  const select = async () => {
    await action({ ids: [id], action: "select", model: "image", metadata: [] });
    await refresh();
  };

  const deselect = async () => {
    await action({
      ids: [id],
      action: "deselect",
      model: "image",
      metadata: [],
    });
    await refresh();
  };

  const loader = <ChaoticOrbit size={25} speed={1.5} color="white" />;
  const label = isSelected ? "Deselect" : "Select";

  return (
    <Box>
      <Button
        color={isSelected ? "warning" : "success"}
        onClick={isSelected ? deselect : select}
      >
        {actionResult.fetching ? loader : label}
      </Button>
    </Box>
  );
};

type ModalProps = {
  close: () => void;
};

const MediaModal = (props: Props & ModalProps) => {
  const { mediaData, kind, close } = props;
  const oids = mediaData.map((r) => r.oid);
  const ids = mediaData.map((r) => r.id);
  const [focused, setFocused] = useState(0);
  const currentId = ids[focused];
  const prefix = "http://localhost:5000";

  const prev = () => {
    setFocused((focused) => {
      if (focused > 0) {
        return focused - 1;
      }

      return oids.length - 1;
    });
  };

  const next = () => {
    setFocused((focused) => {
      if (focused < oids.length - 1) {
        return focused + 1;
      }

      return 0;
    });
  };

  const [actionResult, action] = useDoActionMutation();

  const deleteCurrent = async () => {
    await action({
      ids: [currentId],
      action: "delete",
      model: kind,
      metadata: [],
    });
    next();
    /* await refresh({ requestPolicy: "network-only" }); */
  };

  const src = `${prefix}/image/${currentId}`;
  let el = <img alt="img" width={512} height={512} src={src} key={src} />;

  if (kind === "video") {
    const src = `${prefix}/video/${currentId}`;
    el = (
      <video controls autoPlay key={src}>
        <source type="video/mp4" src={src} />
      </video>
    );
  }

  const label = `${focused + 1} / ${oids.length}`;

  let extraControls = <ExtraControlsImage id={currentId} />;
  if (kind === "video") {
    extraControls = <ExtraControlsVideo id={currentId} />;
  }

  const modalContent = (
    <Box>
      {el}
      <Box sx={{ justifyContent: "space-evenly", display: "flex" }}>
        {extraControls}
        <Button color="error" onClick={deleteCurrent}>
          Delete
        </Button>
      </Box>
      <Box sx={{ justifyContent: "space-between", display: "flex" }}>
        <IconButton onClick={prev}>
          <ArrowBackIosIcon />
        </IconButton>
        <Typography component="div" sx={{ margin: "auto" }}>
          {label}
        </Typography>
        <IconButton onClick={next}>
          <ArrowForwardIosIcon />
        </IconButton>
      </Box>
    </Box>
  );

  return (
    <Modal
      open={true}
      onClose={close}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box component="div" sx={style}>
        {modalContent}
      </Box>
    </Modal>
  );
};

export const MediaViewer = (props: Props) => {
  const { mediaData, kind } = props;
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <Box>
      {modalOpen && <MediaModal {...props} close={() => setModalOpen(false)} />}
      {mediaData.length > 0 && (
        <>
          {mediaData.length}
          <IconButton onClick={() => setModalOpen(true)}>
            <PlayCircleIcon />
          </IconButton>
        </>
      )}
    </Box>
  );
};
