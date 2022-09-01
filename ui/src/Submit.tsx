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
import Slider from "@mui/material/Slider";

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
  const [count, setCount] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);

  const [createResult, create] = useCreateRequestMutation();
  const { fetching } = createResult;

  const submit = async () => {
    if (prompt.length > 0) {
      await create({ prompt, count });
      setModalOpen(false);
      setPrompt("");
      setCount(1);
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
          <TextField
            label="Prompt"
            variant="outlined"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          Schedule #{count} tasks
          <Slider
            aria-label="Volume"
            value={count}
            min={1}
            max={15}
            onChange={(e, v) => setCount(v as number)}
          />
          {!fetching && <Button onClick={submit}>Submit</Button>}
          {fetching && (
            <Box sx={{ display: "flex", justifyContent: "center" }}>
              <ChaoticOrbit size={25} speed={1.5} color="white" />
            </Box>
          )}
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
