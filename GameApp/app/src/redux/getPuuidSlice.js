import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// 비동기 요청을 위한 Thunk
export const fetchPuuid = createAsyncThunk(
  "getPuuid/fetchPuuid",
  async (summonerName) => {
    const [ganeName, tagLine = ""] = summonerName.split("-");
    const response = await axios.get(
      `http://127.0.0.1:8000/v1/users/puuid?gameName=${ganeName}&tagLine=${tagLine}`
    );
    return response.data;
  }
);

const getPuuidSlice = createSlice({
  name: "getPuuid",
  initialState: {
    result: {},
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPuuid.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPuuid.fulfilled, (state, action) => {
        state.result = action.payload;
        state.loading = false;
      })
      .addCase(fetchPuuid.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default getPuuidSlice.reducer;
