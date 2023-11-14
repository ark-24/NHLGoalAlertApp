import React, { useEffect, useState } from 'react';
import Select from 'react-select';

const App = () => {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);


  useEffect(() => {
   
const fetchTeams = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/nhl-proxy');
    const data = await response.json();
    let teams = []
    data?.forEach((team) => {if (team.lastSeason === null) teams.push({ id: team.id,name: team.fullName })});
    setTeams(teams);
  } catch (error) {
    console.error('Error fetching teams:', error);
    throw error; // Rethrow the error so it can be handled in the calling function, if needed
  }
};

fetchTeams();
  }, []);
  const saveTeams = async () => {
    const postData = {...selectedTeam}
    try {
      const response = await fetch(`http://localhost:8080/api/saveTeams`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(postData),
        });
        if (response.ok) {
          const data = await response.json();
        }
  } catch (error) {
    console.log(error);
  }
  }
  

  return (
    <div style={{ display: 'flex', alignItems: 'center', }}>
      {teams.length > 0 && (
        <div style={{width: '1000px', align: 'center' ,marginLeft:'300px'}}>
        <Select
        onChange={setSelectedTeam}
          options={teams?.map((team) => ({ value: team.id, label: team.name }))}
          minMenuHeight={1900}
        />
        </div>
      )}
      <button onClick={() => saveTeams()}>click</button>
    </div>
  );
};

export default App;
