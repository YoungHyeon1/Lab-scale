import SidebarComponent from "./SidebarComponent";
import { SearchBar } from "./SearchBar";
import React, {useState} from "react";
import { useSelector } from "react-redux";
import styled from "styled-components";
const CardContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20px;
`;

const Card = styled.div`
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 200px;
  margin: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }
`;


const CardHeader = styled.div`
  background: #007bff;
  color: #fff;
  padding: 10px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  font-size: 1.2em;
`;

const CardBody = styled.div`
  padding: 10px;
`;

const CardTitle = styled.h3`
  margin: 0;
  font-size: 1.1em;
`;

const CardText = styled.p`
  margin: 5px 0;
  color: #555;
`;

const Research = () => {
   
    const [showModal, setShowModal] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const { stats } = useSelector((state) => state.gameStats);
    const handleSearchError = (message) => {
      setErrorMessage(message);
      setShowModal(true);
    };
    const handleClose = () => setShowModal(false);

    const sampleData = [
        { header: 'Header 1', title: 'Title 1', text: 'This is some sample text for card 1.' },
        { header: 'Header 2', title: 'Title 2', text: 'This is some sample text for card 2.' },
        { header: 'Header 3', title: 'Title 3', text: 'This is some sample text for card 3.' },
      ];
      
 
  
    return(
        <>
        <SidebarComponent />
        <SearchBar onError={handleSearchError} />
        <div className="profile-bar">
            <img src="profile.jpg" alt="" className="profile-image" />
            <span className="profile-name">John Doe</span>
        </div>
        
        <CardContainer>
        {sampleData.map((item, index) => (
            <Card key={index}>
            <CardHeader>{item.header}</CardHeader>
            <CardBody>
                <CardTitle>{item.title}</CardTitle>
                <CardText>{item.text}</CardText>
            </CardBody>
            </Card>
        ))}
        </CardContainer>

        </>
    )
    
}

export default Research