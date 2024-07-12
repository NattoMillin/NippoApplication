import { TextField } from "@mui/material";
import { FormikProps } from "formik";

interface FormikTextFieldProps<T> {
  name: keyof T;
  label: string;
  formik: FormikProps<T>;
  variant?: "outlined" | "filled" | "standard";
  type?: "text" | "password";
  autoComplete?: "new-password";
}

// ジェネリック型をコンポーネントに適用
export const FormikTextField = <T extends {}>(
  props: FormikTextFieldProps<T>
) => {
  return (
    <TextField
      size="small"
      id={String(props.name)}
      name={String(props.name)}
      label={String(props.label)}
      type={String(props.type)}
      autoComplete={String(props.autoComplete)}
      variant={props.variant}
      fullWidth
      value={props.formik.values[props.name]}
      onChange={props.formik.handleChange}
      onBlur={props.formik.handleBlur}
      error={
        !!(props.formik.touched[props.name] && props.formik.errors[props.name])
      }
      helperText={String(
        props.formik.touched[props.name] && props.formik.errors[props.name]
          ? props.formik.errors[props.name]
          : ""
      )}
    />
  );
};
