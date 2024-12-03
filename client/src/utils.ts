export const ping = async (): Promise<void> => {
  const url = "http://localhost:8080/ping";
  const response = await fetch(url);

  if (response.ok === false) {
    alert("Ping failed :(");
    return;
  }

  const json = await response.json();

  console.log("successfully pinged:", json);
};
