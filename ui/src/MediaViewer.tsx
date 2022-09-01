import React, { useState } from "react";
import { useLargeObjectsQuery } from "./generated/graphql";

import Box from "@mui/material/Box";
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

type Props = {
  oids: Array<number>;
  kind: "video" | "image";
};

type ModalProps = {
  close: () => void;
};

const MediaModal = (props: Props & ModalProps) => {
  const { oids, kind, close } = props;
  const [focused, setFocused] = useState(0);
  const current = oids[focused];

  const [result, refresh] = useLargeObjectsQuery({
    variables: { oids: [current] },
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

  let prefix = "data:image/png;base64,";
  const mediaData = allData[0];
  const src = `${prefix}${mediaData}`;
  let el = <img width={512} height={512} src={src} />;

  if (kind === "video") {
    prefix = "data:video/mp4;base64,";
    const src = `${prefix}${mediaData}`;
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
  const { oids, kind } = props;
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <Box>
      {modalOpen && <MediaModal {...props} close={() => setModalOpen(false)} />}
      {oids.length > 0 && (
        <IconButton onClick={() => setModalOpen(true)}>
          <PlayCircleIcon />
        </IconButton>
      )}
    </Box>
  );
};
