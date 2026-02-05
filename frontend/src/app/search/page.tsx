"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useState, useEffect, Suspense } from "react";
import { useQuery } from "@tanstack/react-query";
import { Loader2, BarChart3 } from "lucide-react";
import { Header, Footer } from "@/components/layout/header";
import { SearchBox } from "@/components/search/search-box";
import { FilterPanel, PROPERTY_TYPES } from "@/components/search/filter-panel";
import { ListingCard, ListingCardSkeleton } from "@/components/listings/listing-card";
import { Button } from "@/components/ui/button";
import { searchListings, getSearchHistory, type SearchRequest } from "@/lib/api";
import { formatDistanceToNow } from "date-fns";
import { vi } from "date-fns/locale";

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialQuery = searchParams.get("q") || "";

  const [activeTab, setActiveTab] = useState<"ai" | "history">("ai");
  const [query, setQuery] = useState(initialQuery);
  /* Manual Search Trigger Logic:
   * 1. `filters` state matches the UI dropdowns (Pending)
   * 2. `appliedFilters` matches what is sent to the API (Active)
   * 3. `handleSearch` commits `filters` -> `appliedFilters`
   */
  const [filters, setFilters] = useState<{
    district?: string;
    property_type?: string;
    price_min?: string;
    price_max?: string;
    area_min?: string;
    area_max?: string;
  }>({});

  const [appliedFilters, setAppliedFilters] = useState(filters);

  // Track if search has been explicitly triggered by user or URL
  const [isSearchTriggered, setIsSearchTriggered] = useState(!!initialQuery);

  // Helper to build query from filters
  const buildQueryFromFilters = () => {
    if (query) return query; // User typed something -> Use it

    const parts = [];

    // 1. Property Type
    if (appliedFilters.property_type) {
      const pType = PROPERTY_TYPES.find(t => t.value === appliedFilters.property_type);
      if (pType) parts.push(pType.label);
    }

    // 2. District
    if (appliedFilters.district) {
      parts.push(appliedFilters.district);
    }

    // Join parts or fallback
    return parts.length > 0 ? parts.join(" ") : "Bất động sản";
  };

  const searchRequest: SearchRequest = {
    query: buildQueryFromFilters(),
    filters: {
      district: appliedFilters.district,
      property_type: appliedFilters.property_type,
      min_price: appliedFilters.price_min ? parseInt(appliedFilters.price_min) : undefined,
      max_price: appliedFilters.price_max ? parseInt(appliedFilters.price_max) : undefined,
      min_area: appliedFilters.area_min ? parseInt(appliedFilters.area_min) : undefined,
      max_area: appliedFilters.area_max ? parseInt(appliedFilters.area_max) : undefined,
    },
    max_results: 20,
    search_realtime: true,
  };

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["search", searchRequest],
    queryFn: () => searchListings(searchRequest),
    enabled: isSearchTriggered && !!searchRequest.query, // Only search if triggered AND valid query
  });

  const { data: historyItems, isLoading: historyLoading } = useQuery({
    queryKey: ["searchHistory"],
    queryFn: () => getSearchHistory(),
    enabled: activeTab === "history",
  });

  // Sync AI-inferred filters to UI AND Applied State
  // When AI returns new filters, we assume they are "accepted" until user changes them
  useEffect(() => {
    if (data?.applied_filters) {
      const af = data.applied_filters;
      setFilters(prev => {
        const next = { ...prev };
        let changed = false;

        if (af.district && prev.district !== af.district) {
          next.district = af.district;
          changed = true;
        }
        if (af.property_type && prev.property_type !== af.property_type) {
          next.property_type = af.property_type;
          changed = true;
        }
        if (af.min_price && prev.price_min !== af.min_price.toString()) {
          next.price_min = af.min_price.toString();
          changed = true;
        }
        if (af.max_price && prev.price_max !== af.max_price.toString()) {
          next.price_max = af.max_price.toString();
          changed = true;
        }

        if (changed) {
          // Also update applied filters to avoid double-search or state mismatch
          setAppliedFilters(next);
          return next;
        }
        return prev;
      });
    }
  }, [data]);

  const handleSearch = (newQuery: string) => {
    setQuery(newQuery);
    setAppliedFilters(filters); // Commit pending UI filters to active search
    setIsSearchTriggered(true); // Trigger search
  };

  const handleReset = () => {
    setQuery("");
    setFilters({});
    setAppliedFilters({});
    setIsSearchTriggered(false); // Reset search trigger
    // Optional: Refresh query to default state if needed, but empty state usually handles it
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1 container py-8">
        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b">
          <button
            onClick={() => setActiveTab("ai")}
            className={`px-4 py-2 font-medium transition-colors ${activeTab === "ai"
              ? "border-b-2 border-primary text-primary"
              : "text-muted-foreground hover:text-foreground"
              }`}
          >
            Tìm kiếm AI
          </button>
          <button
            onClick={() => setActiveTab("history")}
            className={`px-4 py-2 font-medium transition-colors ${activeTab === "history"
              ? "border-b-2 border-primary text-primary"
              : "text-muted-foreground hover:text-foreground"
              }`}
          >
            Lịch sử tìm kiếm
          </button>
        </div>

        {/* AI Search Tab */}
        {activeTab === "ai" && (
          <>
            <div className="mb-6">
              <SearchBox
                defaultValue={query}
                onSearch={handleSearch}
                onReset={handleReset}
                placeholder="Nhập yêu cầu tìm kiếm của bạn..."
              />
            </div>

            <div className="mb-6">
              <FilterPanel
                filters={filters}
                onChange={setFilters}
                onReset={() => setFilters({})}
              />
            </div>

            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">
                {(() => {
                  // Dynamic Title Generation
                  const isGenericQuery = !query || query.toLowerCase() === "bất động sản";
                  if (isGenericQuery && (filters.district || filters.property_type)) {
                    const typeLabel = PROPERTY_TYPES.find(t => t.value === filters.property_type)?.label || "Bất động sản";
                    const districtLabel = filters.district ? `tại ${filters.district}` : "";
                    return `Kết quả tìm kiếm ${typeLabel} ${districtLabel}`;
                  }
                  return query ? `Kết quả tìm kiếm "${query}"` : "Nhập từ khóa để tìm kiếm";
                })()}
              </h2>
              {data && (
                <span className="text-muted-foreground">
                  {data.total} kết quả ({data.execution_time_ms}ms)
                </span>
              )}
            </div>

            {isLoading && (
              <div className="flex flex-col items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <p className="mt-4 text-muted-foreground">
                  AI đang tìm kiếm trên các nền tảng...
                </p>
              </div>
            )}

            {isError && (
              <div className="text-center py-12">
                <p className="text-destructive">Đã xảy ra lỗi: {(error as Error).message}</p>
              </div>
            )}

            {!isLoading && query && data?.results?.length === 0 && (
              <div className="text-center py-12">
                <p className="text-muted-foreground">
                  Không tìm thấy kết quả phù hợp. Thử thay đổi từ khóa hoặc bộ lọc.
                </p>
              </div>
            )}

            {data?.results && data.results.length > 0 && (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {data.results.map((listing) => (
                  <ListingCard key={listing.id} listing={listing} />
                ))}
              </div>
            )}

            {!query && !isLoading && (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {Array.from({ length: 6 }).map((_, i) => (
                  <ListingCardSkeleton key={i} />
                ))}
              </div>
            )}
          </>
        )}

        {/* History Tab */}
        {activeTab === "history" && (
          <div className="max-w-4xl mx-auto py-8">
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-bold">Lịch sử tìm kiếm</h2>
            </div>

            {historyLoading ? (
              <div className="flex justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : historyItems && historyItems.length > 0 ? (
              <div className="space-y-4">
                {historyItems.map((item: any) => (
                  <div
                    key={item.id}
                    className="p-4 border rounded-lg hover:bg-muted/50 transition-colors cursor-pointer group"
                    onClick={() => {
                      setQuery(item.query);
                      // Merging filters if any
                      if (item.filters) {
                        setFilters({
                          district: item.filters.district,
                          property_type: item.filters.property_type,
                          price_min: item.filters.price_min?.toString(),
                          price_max: item.filters.price_max?.toString(),
                        });
                      }
                      setActiveTab("ai");
                      setIsSearchTriggered(true);
                    }}
                  >
                    <div className="flex justify-between items-start mb-1">
                      <h4 className="font-semibold text-lg line-clamp-1 group-hover:text-primary transition-colors">
                        {item.query}
                      </h4>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">
                        {formatDistanceToNow(new Date(item.created_at), { addSuffix: true, locale: vi })}
                      </span>
                    </div>
                    <div className="text-sm text-muted-foreground flex gap-3">
                      <span>{item.results_count} kết quả</span>
                      {item.filters?.district && (
                        <span className="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-xs">
                          {item.filters.district}
                        </span>
                      )}
                      {item.filters?.property_type && (
                        <span className="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-xs">
                          {PROPERTY_TYPES.find(t => t.value === item.filters.property_type)?.label || item.filters.property_type}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="flex flex-col items-center justify-center p-8 border border-dashed rounded-lg bg-muted/50">
                  <BarChart3 className="h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-medium text-foreground">Chưa có lịch sử</h3>
                  <p className="text-muted-foreground mt-2 max-w-sm">
                    Các tìm kiếm mới nhất của bạn sẽ xuất hiện tại đây.
                  </p>
                  <Button
                    variant="outline"
                    className="mt-4"
                    onClick={() => setActiveTab("ai")}
                  >
                    Bắt đầu tìm kiếm ngay
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center"><Loader2 className="h-8 w-8 animate-spin" /></div>}>
      <SearchContent />
    </Suspense>
  );
}
