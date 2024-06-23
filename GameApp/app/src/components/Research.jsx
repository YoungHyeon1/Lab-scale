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
import { useState } from "react";

function Research() {
  const { gameName } = useParams();
  const dispatch = useDispatch();

  const { result, userLeague } = useSelector((state) => ({
    result: state.getPuuid.result,
    userLeague: state.userLeague.userLeague,
  }));

  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    dispatch(fetchPuuid(gameName));
  }, [dispatch, gameName]);

  useEffect(() => {
    if (result) {
      dispatch(fetchUserLeague(result.puuid));
    }
  }, [dispatch, result]);

  useEffect(() => {
    if (result && userLeague) {
      setProfileData({
        imageUrl: `https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon${result.profile_icon_id}.jpg`,
        level: result.summoner_level,
        lastUpdated: result.revision_date,
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

  // const profileData = {
  //   imageUrl: `https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon${result.profile_icon_id}.jpg`,
  //   name: result.game_name,
  //   tag: result.tag_line,
  //   level: result.summoner_level,
  //   lastUpdated: result.revision_date,
  //   leagues: userLeague,
  // };
  console.log(userLeague);

  // const profileData = {
  //   imageUrl:
  //     "https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/4529.png",
  //   name: gameName,
  //   rank: "Diamond IV",
  //   rankIconUrl:
  //     "https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/12.png",
  //   lastUpdated: "2023-06-01",
  //   wins: 10,
  //   losses: 1,
  // };

  const gameRecords = [
    {
      id: 1,
      champion: "Ahri",
      team: "Blue",
      result: "Win",
      kills: 9,
      deaths: 1,
      assists: 5,
      date: "2023-06-01",
      detail: [],
    },
    {
      id: 2,
      champion: "Lux",
      team: "Red",
      result: "Loss",
      kills: 2,
      deaths: 4,
      assists: 3,
      date: "2023-06-02",
    },
  ];

  return (
    <>
      <SidebarComponent />
      <SearchBar />
      {console.log(profileData)}
      {profileData ? (
        <>
          <ProfileCard profile={profileData} />
          <GameList games={gameRecords} />
        </>
      ) : (
        <>NotFound</>
      )}
    </>
  );
}

export default Research;
