import { Box, CircularProgress } from "@mui/material";
import React from "react";

interface LoadingProps {
  height?: string;
}

const Loading: React.FC<LoadingProps> = ({ height = "100vh" }) => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height={height}
    >
      <CircularProgress />
    </Box>
  );
};

export default Loading;
