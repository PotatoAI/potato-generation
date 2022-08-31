import React from "react";
import { useAllRequestsQuery } from "./generated/graphql";

function App() {
  const [{ data, fetching, error }] = useAllRequestsQuery();

  return (
    <div>
      <p>{JSON.stringify(data)}</p>
      <p>error {JSON.stringify(error)}</p>
      <p>{fetching ? "fetching" : "done"}</p>
    </div>
  );
}

export default App;
