import React, { useState } from "react";
import { useLargeObjectsQuery, useDoActionMutation } from "./generated/graphql";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";

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

const ExtraControlsImage = (props: { id: string }) => {
  const { id } = props;
  const [actionResult, action] = useDoActionMutation();

  const select = async () => {
    await action({ ids: [id], action: "select", model: "image" });
  };

  const loader = <ChaoticOrbit size={25} speed={1.5} color="white" />;

  return (
    <Box>
      <Button onClick={select}>
        {actionResult.fetching ? loader : "Select"}
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
  const currentOid = oids[focused];

  const [result, refresh] = useLargeObjectsQuery({
    variables: { oids: [currentOid] },
    /* requestPolicy: "network-only", */
  });

  const { fetching, data, error } = result;

  const allData = result.data?.largeObjects?.map((lo) => lo?.data) || [];

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
    await action({ ids: [currentId], action: "delete", model: kind });
    next();
    /* await refresh({ requestPolicy: "network-only" }); */
  };

  let prefix = "data:image/png;base64,";
  const base64Data = allData[0];
  const src = `${prefix}${base64Data}`;
  let el = <img width={512} height={512} src={src} />;

  if (kind === "video") {
    prefix = "data:video/mp4;base64,";
    const src = `${prefix}${base64Data}`;
    el = (
      <video controls autoPlay>
        <source type="video/mp4" src={src} />
      </video>
    );
  }

  const label = `${focused + 1} / ${oids.length}`;

  const loader = (
    <Box sx={{ margin: "auto" }}>
      <ChaoticOrbit size={25} speed={1.5} color="white" />
    </Box>
  );

  let extraControls = <ExtraControlsImage id={currentId} />;

  const modalContent = (
    <Box>
      {!fetching ? (
        el
      ) : (
        <Box
          width="512px"
          height="512px"
          sx={{
            display: "flex",
            justifyContent: "center",
            verticalAlign: "middle",
            padding: "auto",
          }}
        >
          {loader}
        </Box>
      )}
      {error && JSON.stringify(error)}
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
