"use client";

import {
  Avatar,
  Box,
  Button,
  Grid,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import { useFormik } from "formik";
import React, { useLayoutEffect } from "react";
import * as Yup from "yup";

import LockOutlinedIcon from "@mui/icons-material/LockOutlined";

import { Link, useNavigate } from "react-router-dom";
import { useAuthContext } from "./AuthContext";
import { FormikTextField } from "../../components/FormikTextField";
import { fetchAsyncSignup } from "./api";

const Signup: React.FC = () => {
  const { isAuth } = useAuthContext();
  const navigate = useNavigate();
  const validationSchema = Yup.object().shape({
    name: Yup.string().required("Name is required"),
    number: Yup.string().max(6).required("number is required"),
    password: Yup.string()
      .required("Password is required")
      .min(8, "Password must be at least 8 characters long"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password")], "Passwords must match")
      .required("Confirm password is required"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      number: "",
      password: "",
      confirmPassword: "", // 確認用パスワードフィールドを追加
    },
    validationSchema,
    onSubmit: async (state) => {
      await fetchAsyncSignup(state);
      navigate("/");
    },
  });

  useLayoutEffect(() => {
    if (isAuth) {
      navigate("/");
    }
  }, [isAuth, navigate]);

  return (
    <Grid>
      <Paper
        elevation={3}
        sx={{
          p: 4,
          height: "100%",
          width: "360px",
          m: "20px auto",
        }}
      >
        <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
          <Avatar>
            <LockOutlinedIcon />
          </Avatar>
        </Box>
        <Typography>Signup</Typography>
        <form noValidate onSubmit={formik.handleSubmit}>
          <Stack spacing={2}>
            <FormikTextField
              name="name"
              label="Name *"
              variant="standard"
              formik={formik}
            />
            <FormikTextField
              name="number"
              label="従業員番号 *"
              variant="standard"
              formik={formik}
            />
            <FormikTextField
              name="password"
              label="Password *"
              variant="standard"
              type="password"
              autoComplete="new-password"
              formik={formik}
            />
            <FormikTextField
              name="confirmPassword"
              label="Confirm Password *"
              variant="standard"
              type="password"
              autoComplete="new-password"
              formik={formik}
            />
            <Button fullWidth variant="contained" type="submit">
              Submit
            </Button>
            <Link to={"/signin"}>Or Sign in</Link>
          </Stack>
        </form>
      </Paper>
    </Grid>
  );
};

export default Signup;
