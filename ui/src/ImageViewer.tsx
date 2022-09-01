import React, { useState } from "react";
import { useLargeObjectsQuery } from "./generated/graphql";

import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";

import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
};

export const ImageViewer = (props: { oids: Array<number> }) => {
  const [result, refresh] = useLargeObjectsQuery({
    variables: { oids: props.oids },
  });

  const { fetching, data, error } = result;

  const allData = result.data?.largeObjects?.map((lo) => lo?.data) || [];
  const [modalOpen, setModalOpen] = useState(false);
  const [focused, setFocused] = useState(0);

  const prevImage = () => {
    setFocused((focused) => {
      if (focused > 0) {
        return focused - 1;
      }

      return allData.length - 1;
    });
  };

  const nextImage = () => {
    setFocused((focused) => {
      if (focused < allData.length - 1) {
        return focused + 1;
      }

      return 0;
    });
  };

  const modal = (
    <Modal
      open={modalOpen}
      onClose={() => setModalOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box component="div" sx={style}>
        <img width={512} height={512} src={allData[focused]} />
        <Box sx={{ justifyContent: "space-between", display: "flex" }}>
          <IconButton onClick={prevImage}>
            <ArrowBackIosIcon />
          </IconButton>
          <Typography component="div" sx={{ margin: "auto" }}>
            {" "}
            {focused + 1} / {allData.length}{" "}
          </Typography>
          <IconButton onClick={nextImage}>
            <ArrowForwardIosIcon />
          </IconButton>
        </Box>
      </Box>
    </Modal>
  );

  return (
    <Box>
      {modal}
      {error && JSON.stringify(error)}
      {!error && allData.length > 0 && (
        <img src={allData[0]} onClick={() => setModalOpen(true)} />
      )}
    </Box>
  );
};
