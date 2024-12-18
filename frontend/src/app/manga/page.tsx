// /frontend/src/app/manga/page.tsx
"use client"
import { useEffect, useState } from 'react';
import { useSession } from "next-auth/react";


type Manga = {
    id: number;
    name: string;
    genre: string;
    status: string;
    score: number | null;
};

const MangaPage = () => {
    const { data: session } = useSession();

    const [mangaList, setMangaList] = useState<Manga[]>([]);
    const [filters, setFilters] = useState({
        name: '',
        genre: '',
        type: [],
        status: []
    });
    const [searchTriggered, setSearchTriggered] = useState(true); // Set to true to load manga
    const [pagination, setPagination] = useState({
        total: 0,
        pages: 0,
        currentPage: 1
    });

    const handleAddToList = async (mangaId: number, listType: string) => {
        try {
            const response = await fetch("http://localhost:3000/api/auth/session");
            const sessionData = await response.json();
    
            const token = sessionData?.accessToken; // Extract JWT from session
            if (!token) throw new Error("Missing authentication token");
    
            const res = await fetch("http://127.0.0.1:5000/api/manga_list", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`, // Send JWT to Flask
                },
                body: JSON.stringify({ manga_id: mangaId, list_type: listType }),
            });

            const result = await res.json();
            console.log("Response Body:", result); // Debug response body
    
            if (res.status === 401) {
                alert("Unauthorized. Please log in again.");
                return;
            }
    
            if (!res.ok) {
                throw new Error("Failed to add manga to list.");
            }
    
            alert(`Successfully added to ${listType} list!`);
        } catch (error) {
            console.error("Error adding manga to list:", error);
            alert("An error occurred. Please try again.");
        }
    };
    

    // Handle input changes
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFilters(prevFilters => ({
            ...prevFilters,
            [name]: value
        }));
    };

    // Handle checkbox changes for type and status dropdowns
    const handleCheckboxChange = (
        e: React.ChangeEvent<HTMLSelectElement>, 
        filterType: 'type' | 'status'
    ) => {
        const { selectedOptions } = e.target;
        const selectedValues = Array.from(selectedOptions).map(option => option.value);

        setFilters(prevFilters => ({
            ...prevFilters,
            [filterType]: selectedValues
        }));
    };

    const handleClearFilters = () => {
        setFilters({
            name: '',
            genre: '',
            type: [],
            status: []
        });
        setPagination({
            total: 0,
            pages: 0,
            currentPage: 1
        });
        setSearchTriggered(true);  // Trigger search to reload data with empty filters
    };
    

    const handleSearchClick = () => {
        setSearchTriggered(true);
    };

    // Fetch data when search is triggered
    useEffect(() => {
        if (!searchTriggered) return;

        const queryParams = new URLSearchParams();

        // Add string fields
        if (filters.name) queryParams.append('name', filters.name);
        if (filters.genre) queryParams.append('genre', filters.genre);

        // Add array fields (type and status) as comma-separated values
        if (filters.type.length > 0) queryParams.append('type', filters.type.join(','));
        if (filters.status.length > 0) queryParams.append('status', filters.status.join(','));

        // Pagination parameters
        const page = pagination.currentPage;
        const per_page = 30;
        queryParams.append('page', page.toString());
        queryParams.append('per_page', per_page.toString());

        // Make the API call with query parameters
        fetch(`http://127.0.0.1:5000/api/manga?${queryParams.toString()}`)
            .then(response => response.json())
            .then(data => {
                setMangaList(data.manga);
                setPagination({
                    total: data.total,
                    pages: data.pages,
                    currentPage: data.current_page
                });
                setSearchTriggered(false);
            })
            .catch(error => console.error('Error fetching manga data:', error));
    }, [searchTriggered, filters, pagination.currentPage]); // Fetch data when filters or page changes

    // Pagination controls
    const handlePageChange = (newPage: number) => {
        setPagination(prev => ({
            ...prev,
            currentPage: newPage
        }));
        setSearchTriggered(true);  // Trigger the search to update the page
    };

    return (
        <div>
            <h1>Manga List</h1>

            {/* Search Filters */}
            <div>
                <input
                    type="text"
                    name="name"
                    value={filters.name}
                    onChange={handleInputChange}
                    placeholder="Search by name"
                />
                <input
                    type="text"
                    name="genre"
                    value={filters.genre}
                    onChange={handleInputChange}
                    placeholder="Search by genre"
                />

                {/* Type Filter */}
                <div>
                    <label>Type:</label>
                    <select
                        multiple
                        value={filters.type}
                        onChange={(e) => handleCheckboxChange(e, 'type')}
                    >
                        <option value="manga">Manga</option>
                        <option value="manhwa">Manhwa</option>
                        <option value="manhua">Manhua</option>
                        <option value="light_novel">LN</option>
                        <option value="novel">Novel</option>
                        <option value="one_shot">OS</option>
                    </select>
                </div>

                {/* Status Filter */}
                <div>
                    <label>Status:</label>
                    <select
                        multiple
                        value={filters.status}
                        onChange={(e) => handleCheckboxChange(e, 'status')}
                    >
                        <option value="finished">Finished</option>
                        <option value="currently_publishing">Ongoing</option>
                        <option value="on_hiatus">Hiatus</option>
                    </select>
                </div>

                {/* Clear Filters Button */}
                <button onClick={handleClearFilters}>Clear</button>

                {/* Search Button */}
                <button onClick={handleSearchClick}>Search</button>
            </div>

            {/* Manga Table */}
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {mangaList.length === 0 ? (
                        <tr>
                            <td colSpan={2}>No manga found</td>
                        </tr>
                    ) : (
                        mangaList.map((manga) => (
                            <tr key={manga.id}>
                                <td>{manga.name}</td>
                                <td>
                                    <button onClick={() => handleAddToList(manga.id, 'reading')}>
                                        Add to Reading
                                    </button>
                                    <button onClick={() => handleAddToList(manga.id, 'completed')}>
                                        Add to Completed
                                    </button>
                                    <button onClick={() => handleAddToList(manga.id, 'dropped')}>
                                        Add to Dropped
                                    </button>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>

            {/* Pagination Controls */}
            <div>
                <button
                    onClick={() => handlePageChange(pagination.currentPage - 1)}
                    disabled={pagination.currentPage === 1}
                >
                    Previous
                </button>
                <span>Page {pagination.currentPage} of {pagination.pages}</span>
                <button
                    onClick={() => handlePageChange(pagination.currentPage + 1)}
                    disabled={pagination.currentPage === pagination.pages}
                >
                    Next
                </button>
            </div>
        </div>
    );
};

export default MangaPage;
