"use client"
// manga.tsx

import { useEffect, useState } from 'react';

type Manga = {
    id: number;
    name: string;
    genre: string;
    status: string;
    score: number | null;
};

const MangaPage = () => {
    const [mangaList, setMangaList] = useState<Manga[]>([]);

    useEffect(() => {
        // Fetch data from Flask API
        fetch('http://127.0.0.1:5000/api/manga')  // Adjust Flask server URL if needed
            .then(response => response.json())
            .then(data => setMangaList(data))
            .catch(error => console.error('Error fetching manga data:', error));
    }, []);

    return (
        <div>
            <h1>Manga List</h1>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Genre</th>
                        <th>Status</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {mangaList.map((manga) => (
                        <tr key={manga.id}>
                            <td>{manga.name}</td>
                            <td>{manga.genre}</td>
                            <td>{manga.status}</td>
                            <td>{manga.score ?? 'N/A'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MangaPage;
