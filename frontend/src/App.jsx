
import { useState } from "react";
import "./App.css";

const recipes = [
  {
    id: 1,
    name: "Paneer Butter Masala",
    cuisine: "North Indian",
    time: "35 min",
    category: "Vegetarian",
    emoji: "🍛",
    color: "peach",
  },
  {
    id: 2,
    name: "Chana Masala",
    cuisine: "Indian",
    time: "30 min",
    category: "Vegan",
    emoji: "🥘",
    color: "sage",
  },
  {
    id: 3,
    name: "Greek Salad",
    cuisine: "Mediterranean",
    time: "15 min",
    category: "Vegetarian",
    emoji: "🥗",
    color: "yellow",
  },
  {
    id: 4,
    name: "Vegetable Fried Rice",
    cuisine: "Asian",
    time: "20 min",
    category: "Vegetarian",
    emoji: "🍚",
    color: "lavender",
  },
];

const tools = [
  {
    icon: "✨",
    title: "AI Cooking Assistant",
    description: "Ask questions and get cooking guidance.",
    link: "#assistant",
  },
  {
    icon: "🥕",
    title: "Manage My Pantry",
    description: "Keep track of ingredients you have.",
    link: "#pantry",
  },
  {
    icon: "🔄",
    title: "Ingredient Substitutions",
    description: "Find alternatives for missing ingredients.",
    link: "#tools",
  },
];

function App() {
  const [search, setSearch] = useState("");

  const filteredRecipes = recipes.filter((recipe) =>
    `${recipe.name} ${recipe.cuisine} ${recipe.category}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <a href="#dashboard" className="brand">
          <div className="brand-icon">🥣</div>
          <div>
            <h2>pantry shef</h2>
            <span>YOUR SMART KITCHEN</span>
          </div>
        </a>

        <div className="sidebar-label">MENU</div>

        <nav className="navigation">
          <a href="#dashboard" className="nav-item active">
            <span>⌂</span> Dashboard
          </a>
          <a href="#recipes" className="nav-item">
            <span>▤</span> Explore Recipes
          </a>
          <a href="#assistant" className="nav-item">
            <span>✧</span> AI Assistant
          </a>
          <a href="#pantry" className="nav-item">
            <span>▧</span> My Pantry
          </a>
          <a href="#tools" className="nav-item">
            <span>⚙</span> Cooking Tools
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-icon">💡</div>
            <h3>Need cooking inspiration?</h3>
            <p>Let AI help you decide what to cook today.</p>
            <a href="#assistant">Try AI Assistant →</a>
          </div>

          <div className="profile">
            <div className="avatar">K</div>
            <div className="profile-info">
              <strong>Home Chef</strong>
              <span>Your kitchen space</span>
            </div>
            <span className="profile-menu">•••</span>
          </div>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div className="breadcrumb">
            My Kitchen <span>/</span> <strong>Dashboard</strong>
          </div>
          <div className="topbar-right">
            <span className="today-label">Your everyday cooking companion</span>
            <div className="top-avatar">K</div>
          </div>
        </header>

        <div className="dashboard-content">
          <section className="welcome-section">
            <div className="welcome-text">
              <span className="eyebrow">YOUR PERSONAL KITCHEN ASSISTANT</span>
              <h1>Good food starts<br />with what you have.</h1>
              <p>
                Discover recipes, manage your pantry and make everyday
                cooking a little easier.
              </p>

              <div className="search-box">
                <span className="search-icon">⌕</span>
                <input
                  type="text"
                  placeholder="Search recipes, ingredients or cuisines..."
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                />
                {search && (
                  <button
                    className="clear-search"
                    onClick={() => setSearch("")}
                    aria-label="Clear search"
                  >
                    ×
                  </button>
                )}
              </div>

              <div className="search-hint">
                <span>Popular:</span>
                <button onClick={() => setSearch("Paneer")}>Paneer</button>
                <button onClick={() => setSearch("Vegan")}>Vegan</button>
                <button onClick={() => setSearch("Rice")}>Rice</button>
              </div>
            </div>

            <div className="welcome-art">
              <div className="art-circle"></div>
              <div className="art-emoji">🥗</div>
              <div className="floating-note note-one">🌿 Fresh ideas</div>
              <div className="floating-note note-two">♡ Made for you</div>
              <div className="art-leaf leaf-one">✦</div>
              <div className="art-leaf leaf-two">✧</div>
            </div>
          </section>

          <section className="section-block" id="recipes">
            <div className="section-heading">
              <div>
                <span className="eyebrow">FIND YOUR NEXT FAVOURITE</span>
                <h2>{search ? "Search Results" : "Explore Recipes"}</h2>
                <p>
                  {search
                    ? `Recipes matching "${search}"`
                    : "A little inspiration for your next meal."}
                </p>
              </div>
              <a href="#recipes" className="text-link">
                View all recipes <span>→</span>
              </a>
            </div>

            {filteredRecipes.length > 0 ? (
              <div className="recipe-grid">
                {filteredRecipes.map((recipe) => (
                  <article className="recipe-card" key={recipe.id}>
                    <div className={`recipe-image ${recipe.color}`}>
                      <span className="recipe-emoji">{recipe.emoji}</span>
                      <span className="recipe-category">{recipe.category}</span>
                      <button
                        className="favorite-button"
                        aria-label={`Save ${recipe.name}`}
                        onClick={(event) => {
                          event.currentTarget.classList.toggle("saved");
                        }}
                      >
                        ♡
                      </button>
                    </div>
                    <div className="recipe-details">
                      <span className="recipe-cuisine">{recipe.cuisine}</span>
                      <h3>{recipe.name}</h3>
                      <div className="recipe-meta">
                        <span>◷ {recipe.time}</span>
                        <span>Easy to prepare</span>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="empty-results">
                <span>🍽️</span>
                <h3>No matching recipes found</h3>
                <p>Try searching for another recipe or ingredient.</p>
                <button onClick={() => setSearch("")}>Clear search</button>
              </div>
            )}
          </section>

          <section className="section-block" id="tools">
            <div className="section-heading">
              <div>
                <span className="eyebrow">MAKE COOKING EASIER</span>
                <h2>Your Kitchen Tools</h2>
                <p>Everything you need, in one place.</p>
              </div>
            </div>

            <div className="tools-grid">
              {tools.map((tool) => (
                <a href={tool.link} className="tool-card" key={tool.title}>
                  <div className="tool-icon">{tool.icon}</div>
                  <div className="tool-info">
                    <h3>{tool.title}</h3>
                    <p>{tool.description}</p>
                  </div>
                  <span className="tool-arrow">↗</span>
                </a>
              ))}
            </div>
          </section>

          <section className="bottom-grid">
            <div className="assistant-panel" id="assistant">
              <div className="assistant-decoration">✦</div>
              <span className="eyebrow">YOUR AI COOKING PARTNER</span>
              <h2>Not sure what to cook?</h2>
              <p>
                Tell Pantry Shef what ingredients you have.
                Get ideas and helpful cooking guidance.
              </p>
              <a href="#assistant" className="primary-button">
                Start a conversation <span>→</span>
              </a>
              <div className="assistant-illustration">👩‍🍳</div>
            </div>

            <div className="pantry-panel" id="pantry">
              <div className="pantry-heading">
                <div>
                  <span className="eyebrow">YOUR INGREDIENTS</span>
                  <h2>My Pantry</h2>
                </div>
                <span className="pantry-icon">🧺</span>
              </div>
              <p>
                Keep your kitchen organised and find recipes using
                ingredients you already have.
              </p>
              <div className="pantry-preview">
                <span>🥔</span>
                <span>🥕</span>
                <span>🥬</span>
                <span>🍅</span>
                <span>+ more</span>
              </div>
              <a href="#pantry" className="text-link">
                Explore my pantry →
              </a>
            </div>
          </section>

          <footer className="footer">
            <span>🥣 pantry shef</span>
            <span>Made for better everyday cooking.</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
