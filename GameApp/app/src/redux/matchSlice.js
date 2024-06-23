import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchMatches = createAsyncThunk(
  "matchesInfo/fetchMatches",
  async ({ puuid, index }) => {
    const response = await axios.get(
      // `http://labscaleloadblancer-1622503253.ap-northeast-2.elb.amazonaws.com/v1/users/matches?puuid=${puuid}`
      `http://localhost:8000/v1/match/?puuid=${puuid}&index=${index}`
    );
    console.log(response);
    if (response.status === 404) {
      return null;
    } else {
      return response.data;
    }
  }
);

const matchesInfoSlice = createSlice({
  name: "match",
  initialState: {
    matches: [],
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
