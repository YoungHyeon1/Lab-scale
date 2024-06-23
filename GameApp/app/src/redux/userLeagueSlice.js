import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchUserLeague = createAsyncThunk(
  "userLeague/fetchUserLeague",
  async (puuid) => {
    const response = await axios.get(
      `http://127.0.0.1:8000/v1/users/league?puuid=${puuid}`
    );
    return response.data;
  }
);

const userLeagueSlice = createSlice({
  name: "userLeague",
  initialState: {
    userLeague: {},
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserLeague.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUserLeague.fulfilled, (state, action) => {
        state.userLeague = action.payload;
        state.loading = false;
      })
      .addCase(fetchUserLeague.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default userLeagueSlice.reducer;
