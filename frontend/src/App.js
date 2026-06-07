import React, { useEffect, useState, useMemo } from "react";
import axios from "axios";
import "./App.css";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
});

function App() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ id: "", name: "", description: "", price: "", quantity: "" });
  const [editId, setEditId] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("");
  const [sortField, setSortField] = useState("id");
  const [sortDirection, setSortDirection] = useState("asc");

  useEffect(() => {
    if (message) { const t = setTimeout(() => setMessage(""), 4000); return () => clearTimeout(t); }
  }, [message]);

  useEffect(() => {
    if (error) { const t = setTimeout(() => setError(""), 4000); return () => clearTimeout(t); }
  }, [error]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get("/products/");
      setProducts(res.data);
      setError("");
    } catch {
      setError("Failed to fetch products.");
    }
    setLoading(false);
  };

  useEffect(() => { fetchProducts(); }, []);

  const stats = useMemo(() => {
    const total = products.length;
    const units = products.reduce((s, p) => s + p.quantity, 0);
    const value = products.reduce((s, p) => s + p.price * p.quantity, 0);
    const avg = units ? value / units : 0;
    return { total, units, value, avg };
  }, [products]);

  const handleSort = (field) => {
    if (sortField === field) setSortDirection(d => d === "asc" ? "desc" : "asc");
    else { setSortField(field); setSortDirection("asc"); }
  };

  const filteredProducts = useMemo(() => {
    const q = filter.trim().toLowerCase();
    let list = q
      ? products.filter(p =>
          String(p.id).includes(q) ||
          p.name?.toLowerCase().includes(q) ||
          p.description?.toLowerCase().includes(q)
        )
      : [...products];
    return list.sort((a, b) => {
      let av = a[sortField], bv = b[sortField];
      if (typeof av === "number") return sortDirection === "asc" ? av - bv : bv - av;
      return sortDirection === "asc"
        ? String(av).localeCompare(String(bv))
        : String(bv).localeCompare(String(av));
    });
  }, [products, filter, sortField, sortDirection]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const resetForm = () => {
    setForm({ id: "", name: "", description: "", price: "", quantity: "" });
    setEditId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(""); setError("");
    try {
      const payload = { ...form, id: Number(form.id), price: Number(form.price), quantity: Number(form.quantity) };
      if (editId) {
        await api.put(`/products/${editId}`, payload);
        setMessage("Product updated successfully.");
      } else {
        await api.post("/products/", payload);
        setMessage("Product added successfully.");
      }
      resetForm();
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.detail || "Operation failed.");
    }
    setLoading(false);
  };

  const handleEdit = (p) => {
    setForm({ id: p.id, name: p.name, description: p.description, price: p.price, quantity: p.quantity });
    setEditId(p.id);
    setMessage(""); setError("");
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this product?")) return;
    setLoading(true);
    try {
      await api.delete(`/products/${id}`);
      setMessage("Product deleted.");
      fetchProducts();
    } catch {
      setError("Delete failed.");
    }
    setLoading(false);
  };

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <span className="sort-icon">↕</span>;
    return <span className="sort-icon active">{sortDirection === "asc" ? "↑" : "↓"}</span>;
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-brand">
          <span className="header-icon">▤</span>
          <span className="header-title">Inventory Manager</span>
        </div>
        <button className="btn btn-outline" onClick={fetchProducts} disabled={loading}>
          ↻ Refresh
        </button>
      </header>

      <main className="main">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total products</div>
            <div className="stat-value">{stats.total}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total value</div>
            <div className="stat-value">${Math.round(stats.value).toLocaleString()}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total units</div>
            <div className="stat-value">{stats.units}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg price/unit</div>
            <div className="stat-value">${Math.round(stats.avg)}</div>
          </div>
        </div>

        <div className="content-grid">
          <div className="card form-card">
            <div className="card-title">{editId ? "Edit product" : "Add product"}</div>
            <form onSubmit={handleSubmit} className="form">
              <div className="field">
                <label>ID</label>
                <input type="number" name="id" placeholder="e.g. 7" value={form.id} onChange={handleChange} required disabled={!!editId} />
              </div>
              <div className="field">
                <label>Name</label>
                <input type="text" name="name" placeholder="Product name" value={form.name} onChange={handleChange} required />
              </div>
              <div className="field">
                <label>Description</label>
                <input type="text" name="description" placeholder="Short description" value={form.description} onChange={handleChange} required />
              </div>
              <div className="field">
                <label>Price ($)</label>
                <input type="number" name="price" placeholder="0.00" step="0.01" value={form.price} onChange={handleChange} required />
              </div>
              <div className="field">
                <label>Quantity</label>
                <input type="number" name="quantity" placeholder="0" value={form.quantity} onChange={handleChange} required />
              </div>
              <div className="form-actions">
                <button className="btn btn-primary" type="submit" disabled={loading}>
                  {editId ? "Update" : "Add"}
                </button>
                {editId && (
                  <button className="btn btn-outline" type="button" onClick={() => { resetForm(); setMessage(""); setError(""); }}>
                    Cancel
                  </button>
                )}
              </div>
              {message && <div className="msg msg-success">{message}</div>}
              {error && <div className="msg msg-error">{error}</div>}
            </form>
          </div>

          <div className="card table-card">
            <div className="toolbar">
              <div className="search-box">
                <span className="search-icon">⌕</span>
                <input
                  type="text"
                  placeholder="Search by id, name or description..."
                  value={filter}
                  onChange={e => setFilter(e.target.value)}
                />
              </div>
              <span className="count-badge">{filteredProducts.length} items</span>
            </div>

            {loading ? (
              <div className="loader">Loading...</div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th onClick={() => handleSort("id")}>ID <SortIcon field="id" /></th>
                      <th onClick={() => handleSort("name")}>Name <SortIcon field="name" /></th>
                      <th>Description</th>
                      <th onClick={() => handleSort("price")}>Price <SortIcon field="price" /></th>
                      <th onClick={() => handleSort("quantity")}>Qty <SortIcon field="quantity" /></th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredProducts.length === 0 ? (
                      <tr><td colSpan={6} className="empty">No products found.</td></tr>
                    ) : (
                      filteredProducts.map(p => (
                        <tr key={p.id}>
                          <td className="td-id">#{p.id}</td>
                          <td className="td-name">{p.name}</td>
                          <td className="td-desc" title={p.description}>{p.description}</td>
                          <td className="td-price">${Number(p.price).toFixed(2)}</td>
                          <td><span className="qty-badge">{p.quantity}</span></td>
                          <td>
                            <div className="row-actions">
                              <button className="btn-action btn-edit" onClick={() => handleEdit(p)}>Edit</button>
                              <button className="btn-action btn-delete" onClick={() => handleDelete(p.id)}>Delete</button>
                            </div>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;