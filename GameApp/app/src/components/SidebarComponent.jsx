import React, { useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const SidebarContainer = styled.div`
  width: ${(props) => (props.isOpen ? "250px" : "0")};
  height: 100vh;
  background-color: #333;
  overflow-x: hidden;
  transition: 0.5s;
  position: fixed;
  z-index: 1;
  right: 0;
  top: 0;
`;

const SidebarButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  right: ${(props) => (props.isOpen ? "250px" : "0")};
  top: 20px;
  width: 40px;
  height: 40px;
  background-color: #444;
  color: white;
  border: none;
  cursor: pointer;
  z-index: 2;
  transition: 0.5s;
`;

const MenuItem = styled(Link)`
  padding: 10px 15px;
  text-decoration: none;
  font-size: 25px;
  color: white;
  display: block;
  transition: 0.3s;
  &:hover {
    background-color: #ddd;
    color: black;
  }
`;

const SidebarComponent = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <SidebarButton onClick={toggleSidebar} isOpen={isOpen}>
        {isOpen ? "Close" : "Menu"}
      </SidebarButton>
      <SidebarContainer isOpen={isOpen}>
        <MenuItem to="/">홈</MenuItem>
        <MenuItem to="/ai_search">AI 분석</MenuItem>
      </SidebarContainer>
    </>
  );
};

export default SidebarComponent;
