import React, { useState } from "react";
import { useCreateRequestMutation } from "./generated/graphql";

import { ChaoticOrbit } from "@uiball/loaders";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";

import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
};

export const Submit = () => {
  const [prompt, setPrompt] = useState("");
  const [modalOpen, setModalOpen] = useState(false);

  const [createResult, create] = useCreateRequestMutation();
  const { fetching } = createResult;

  const submit = async () => {
    if (prompt.length > 0) {
      await create({ prompt });
      setModalOpen(false);
      setPrompt("");
    }
  };

  const modal = (
    <Modal
      open={modalOpen}
      onClose={() => setModalOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box component="div" sx={style}>
        <Paper
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-evenly",
            padding: "30px",
            width: 300,
            height: 300,
          }}
        >
          {fetching && <ChaoticOrbit size={25} speed={1.5} color="white" />}
          <TextField
            label="Prompt"
            variant="outlined"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <Button onClick={submit}>Submit</Button>
        </Paper>
      </Box>
    </Modal>
  );

  return (
    <Box>
      {modal}
      <Button onClick={() => setModalOpen(true)}>SUBMIT</Button>
    </Box>
  );
};
