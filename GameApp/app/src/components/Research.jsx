import SidebarComponent from "./SidebarComponent";
// import { SearchBar } from "./SearchBar";
import React from "react";
import SearchBar from "./SearchBar";
import ProfileCard from "./module/ProfileCard";
import GameList from "./module/GameList";
import { useParams } from "react-router-dom";

const Research = () => {
  const { gameName } = useParams();

  const profileData = {
    imageUrl:
      "https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/4529.png",
    name: gameName,
    rank: "Diamond IV",
    rankIconUrl:
      "https://ddragon.leagueoflegends.com/cdn/10.6.1/img/profileicon/12.png",
    lastUpdated: "2023-06-01",
    wins: 10,
    losses: 1,
  };

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
      <ProfileCard profile={profileData} />
      <GameList games={gameRecords} />
    </>
  );
};

export default Research;
