import { Box, Container } from "@mui/material";
import Navbar from "../components/Navbar";

type Props = {
  children: React.ReactNode;
};

export default function MainLayout({ children }: Props) {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f7f7f7" }}>
      <Navbar />
      <Container sx={{ py: 4 }}>
        {children}
      </Container>
    </Box>
  );
}