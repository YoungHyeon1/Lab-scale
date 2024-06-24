import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchMatches = createAsyncThunk(
  "matchesInfo/fetchMatches",
  async ({ puuid, index }) => {
    const response = await axios.get(
      // `http://labscaleloadblancer-1622503253.ap-northeast-2.elb.amazonaws.com/v1/users/matches?puuid=${puuid}`
      `http://localhost:8000/v1/match/?puuid=${puuid}&index=${index}`
    );
    if (response.status === 200) {
      return response.data;
    } else {
      return null;
    }
  }
);

const matchesInfoSlice = createSlice({
  name: "match",
  initialState: {
    matches: null,
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMatches.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchMatches.fulfilled, (state, action) => {
        state.matches = action.payload;
        state.loading = false;
      })
      .addCase(fetchMatches.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default matchesInfoSlice.reducer;
