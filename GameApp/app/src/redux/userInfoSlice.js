import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchUserInfo = createAsyncThunk(
  "userInfo/fetchUserInfo",
  async (puuid) => {
    const response = await axios.get(
      `http://127.0.0.1:8000/v1/users/league?puuid=${puuid}`
    );
    return response.data;
  }
);

const userInfoSlice = createSlice({
  name: "userInfo",
  initialState: {
    userInfo: {},
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserInfo.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUserInfo.fulfilled, (state, action) => {
        state.userInfo = action.payload;
        state.loading = false;
      })
      .addCase(fetchUserInfo.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default userInfoSlice.reducer;
