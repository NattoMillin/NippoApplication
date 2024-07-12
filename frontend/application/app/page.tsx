import Image from "next/image";

export default function Home() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Routes>
          <Route path="/" element={<PrivateRoute element={<AppLayout />} />}>
            <Route index element={<Home />} />
          </Route>
          <Route path="/signin" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </ThemeProvider>
    </div>
  );
}
