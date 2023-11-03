import React, { useEffect, useState } from 'react';
import Select from 'react-select';

const App = () => {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);


  useEffect(() => {
   
const fetchTeams = async () => {
  try {
    const response = await fetch('https://statsapi.web.nhl.com/api/v1/teams');
    const data = await response.json();
    const teams = data.teams.map((team) => ({ name: team.name }));
    teams.sort((a, b) => a.name.localeCompare(b.name));
    setTeams(teams);
  } catch (error) {
    console.error('Error fetching teams:', error);
    throw error; // Rethrow the error so it can be handled in the calling function, if needed
  }
};

fetchTeams();
  }, []);
  const saveTeams = async (data) => {
    const postData = {...data}
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
    <div>
      {teams.length > 0 && (
        <Select
        onChange={setSelectedTeam}
          options={teams.map((team) => ({ value: team.name, label: team.name }))}
        />
      )}
      <button onClick={() => console.log(selectedTeam)}>click</button>
    </div>
  );
};

export default App;
