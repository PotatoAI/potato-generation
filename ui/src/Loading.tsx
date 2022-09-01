import React from "react";

import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import { ChaoticOrbit } from "@uiball/loaders";

export const LoadingModal = (props: { loading: boolean }) => {
  const { loading } = props;

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
  };

  return (
    <Modal
      open={loading}
      // eslint-disable-next-line
      onClose={() => {}}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box component="div" sx={style}>
        <ChaoticOrbit size={25} speed={1.5} color="white" />
      </Box>
    </Modal>
  );
};
