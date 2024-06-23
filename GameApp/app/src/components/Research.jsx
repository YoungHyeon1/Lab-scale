import SidebarComponent from "./SidebarComponent";
// import { SearchBar } from "./SearchBar";
import React, { useEffect } from "react";
import SearchBar from "./SearchBar";
import ProfileCard from "./module/ProfileCard";
import GameList from "./module/GameList";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchPuuid } from "../redux/getPuuidSlice";
import { fetchUserLeague } from "../redux/userLeagueSlice";
import { fetchMatches } from "../redux/matchSlice";
import { useState } from "react";

function Research() {
  const { gameName } = useParams();
  const dispatch = useDispatch();
  const { result, userLeague, matches } = useSelector((state) => ({
    result: state.getPuuid.result,
    userLeague: state.userLeague.userLeague,
    matches: state.match.matches,
  }));

  const [profileData, setProfileData] = useState(null);
  const [matchData, setMatchData] = useState(null);
  const [index, setIndex] = useState(1);

  useEffect(() => {
    dispatch(fetchPuuid(gameName));
  }, [dispatch, gameName]);

  useEffect(() => {
    if (result) {
      dispatch(fetchUserLeague(result.puuid));
    }
  }, [dispatch, result]);

  useEffect(() => {
    if (result) {
      dispatch(fetchMatches({ puuid: result.puuid, index }));
    }
  }, [dispatch, result, index]);

  useEffect(() => {
    if (result && Array.isArray(userLeague)) {
      setProfileData({
        imageUrl: `https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon${result.profile_icon_id}.jpg`,
        level: result.summoner_level,
        lastUpdated: result.revision_date,
        name: result.game_name,
        tag: result.tag_line,
        leagues: userLeague.map(
          ({ name, tier, rank, leaguePoints, wins, losses, queue_type }) => ({
            leagueName: name,
            rankIconUrl: `https://opgg-static.akamaized.net/images/medals_new/${tier.toLowerCase()}.png`,
            tier,
            rank,
            wins,
            losses,
            queue_type,
            winRate: Math.round((wins / (wins + losses)) * 100),
            points: leaguePoints,
          })
        ),
      });
    }
  }, [result, userLeague]);

  useEffect(() => {
    if (result && Array.isArray(matches)) {
      setMatchData(matches);
    }
  }, [result, matches]);

  return (
    <>
      <SidebarComponent />
      <SearchBar />
      {profileData ? (
        <>
          <ProfileCard profile={profileData} />
        </>
      ) : (
        <>NotFound</>
      )}
      {matchData && <GameList games={matchData} />}
    </>
  );
}

export default Research;
