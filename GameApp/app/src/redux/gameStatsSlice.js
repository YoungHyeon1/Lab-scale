import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// 비동기 요청을 위한 Thunk
export const fetchGameStats = createAsyncThunk(
  "gameStats/fetchGameStats",
  async (summonerName) => {
    const response = await axios.get(
      `https://api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}`
    );
    return response.data;
  }
);

const gameStatsSlice = createSlice({
  name: "gameStats",
  initialState: {
    stats: {},
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchGameStats.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchGameStats.fulfilled, (state, action) => {
        state.stats = action.payload;
        state.loading = false;
      })
      .addCase(fetchGameStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default gameStatsSlice.reducer;
