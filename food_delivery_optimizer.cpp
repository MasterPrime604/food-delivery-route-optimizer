/**
 * Food Polar Bear - Delivery Route Optimization System (FINAL FIXED VERSION)
 * Completely debugged and working implementation
 */

#include <iostream>
#include <fstream>
#include <cstring>
#include <climits>

using namespace std;

const int MAX_NODES = 10000;
const int MAX_REST = 50;
const int MAX_ORD = 100;
const int MAX_RID = 20;

struct Order {
    char name[100];
    int location;
    int timeLimit;
    bool assigned;
};

struct Restaurant {
    char name[100];
    int location;
    Order orders[MAX_ORD];
    int orderCount;
};

class GridGraph {
private:
    int** adj;
    int size;
    int total;
    int* dist;
    int* pred;
    
public:
    GridGraph(int n) : size(n), total(n*n) {
        // Allocate adjacency matrix
        adj = new int*[total + 1];
        for (int i = 0; i <= total; i++) {
            adj[i] = new int[total + 1]();
        }
        dist = new int[total + 1];
        pred = new int[total + 1];
        createGraph();
    }
    
    ~GridGraph() {
        for (int i = 0; i <= total; i++) {
            delete[] adj[i];
        }
        delete[] adj;
        delete[] dist;
        delete[] pred;
    }
    
    void createGraph() {
        for (int node = 1; node <= total; node++) {
            int row = (node - 1) / size;
            int col = (node - 1) % size;
            
            if (col < size - 1) {
                int right = node + 1;
                adj[node][right] = adj[right][node] = 1;
            }
            if (row < size - 1) {
                int bottom = node + size;
                adj[node][bottom] = adj[bottom][node] = 1;
            }
        }
    }
    
    void bfs(int start) {
        for (int i = 0; i <= total; i++) {
            dist[i] = -1;
            pred[i] = -1;
        }
        
        int* queue = new int[total + 1];
        int front = 0, rear = 0;
        
        dist[start] = 0;
        queue[rear++] = start;
        
        while (front < rear) {
            int curr = queue[front++];
            for (int i = 1; i <= total; i++) {
                if (adj[curr][i] == 1 && dist[i] == -1) {
                    dist[i] = dist[curr] + 1;
                    pred[i] = curr;
                    queue[rear++] = i;
                }
            }
        }
        delete[] queue;
    }
    
    int getDistance(int s, int d) {
        if (s == d) return 0;
        bfs(s);
        return dist[d];
    }
    
    void getPath(int s, int d, int* path, int& len) {
        if (s == d) {
            path[0] = s;
            len = 1;
            return;
        }
        bfs(s);
        
        int temp[MAX_NODES];
        int tlen = 0;
        int curr = d;
        while (curr != -1) {
            temp[tlen++] = curr;
            curr = pred[curr];
        }
        
        len = tlen;
        for (int i = 0; i < len; i++) {
            path[i] = temp[len - 1 - i];
        }
    }
};

struct RouteStop {
    int location;
    char name[100];
    bool isNamed;
};

class RouteOptimizer {
private:
    GridGraph* graph;
    Restaurant* rests;
    int numRests;
    int numRiders;
    
    RouteStop** routes;
    int* routeLens;
    int* routeTimes;
    
    struct Assign {
        Restaurant* rest;
        Order* order;
    };
    
    Assign** assignments;
    int* assignCounts;
    
public:
    RouteOptimizer(GridGraph* g, Restaurant* r, int nr, int nrid) {
        graph = g;
        rests = r;
        numRests = nr;
        numRiders = nrid;
        
        routes = new RouteStop*[numRiders];
        routeLens = new int[numRiders]();
        routeTimes = new int[numRiders]();
        assignments = new Assign*[numRiders];
        assignCounts = new int[numRiders]();
        
        for (int i = 0; i < numRiders; i++) {
            routes[i] = new RouteStop[MAX_NODES];
            assignments[i] = new Assign[MAX_ORD];
        }
    }
    
    ~RouteOptimizer() {
        for (int i = 0; i < numRiders; i++) {
            delete[] routes[i];
            delete[] assignments[i];
        }
        delete[] routes;
        delete[] routeLens;
        delete[] routeTimes;
        delete[] assignments;
        delete[] assignCounts;
    }
    
    void optimize() {
        struct OrdInfo {
            Restaurant* rest;
            Order* order;
        };
        
        OrdInfo* allOrds = new OrdInfo[MAX_REST * MAX_ORD];
        int numOrds = 0;
        
        for (int i = 0; i < numRests; i++) {
            for (int j = 0; j < rests[i].orderCount; j++) {
                allOrds[numOrds].rest = &rests[i];
                allOrds[numOrds].order = &rests[i].orders[j];
                numOrds++;
            }
        }
        
        // Sort by time limit
        for (int i = 0; i < numOrds - 1; i++) {
            for (int j = 0; j < numOrds - i - 1; j++) {
                if (allOrds[j].order->timeLimit > allOrds[j + 1].order->timeLimit) {
                    OrdInfo temp = allOrds[j];
                    allOrds[j] = allOrds[j + 1];
                    allOrds[j + 1] = temp;
                }
            }
        }
        
        // Assign to riders
        for (int i = 0; i < numOrds; i++) {
            Restaurant* rest = allOrds[i].rest;
            Order* ord = allOrds[i].order;
            
            int timeDist = graph->getDistance(rest->location, ord->location);
            if (timeDist > ord->timeLimit) continue;
            
            int bestRider = 0;
            int minTime = routeTimes[0];
            
            for (int r = 1; r < numRiders; r++) {
                if (routeTimes[r] < minTime) {
                    minTime = routeTimes[r];
                    bestRider = r;
                }
            }
            
            assignments[bestRider][assignCounts[bestRider]].rest = rest;
            assignments[bestRider][assignCounts[bestRider]].order = ord;
            assignCounts[bestRider]++;
            ord->assigned = true;
        }
        
        delete[] allOrds;
        
        // Build routes
        for (int i = 0; i < numRiders; i++) {
            if (assignCounts[i] > 0) {
                buildRoute(i);
            }
        }
    }
    
    void buildRoute(int rid) {
        Restaurant* uRests[MAX_REST];
        Order* rOrds[MAX_REST][MAX_ORD];
        int rOrdCnts[MAX_REST];
        int numUR = 0;
        
        for (int i = 0; i < assignCounts[rid]; i++) {
            Restaurant* rest = assignments[rid][i].rest;
            Order* ord = assignments[rid][i].order;
            
            int idx = -1;
            for (int j = 0; j < numUR; j++) {
                if (uRests[j] == rest) {
                    idx = j;
                    break;
                }
            }
            
            if (idx == -1) {
                uRests[numUR] = rest;
                rOrdCnts[numUR] = 0;
                idx = numUR;
                numUR++;
            }
            
            rOrds[idx][rOrdCnts[idx]++] = ord;
        }
        
        int curLoc = 0;
        bool visited[MAX_REST] = {false};
        routeLens[rid] = 0;
        routeTimes[rid] = 0;
        
        for (int i = 0; i < numUR; i++) {
            int nearIdx = -1;
            int minDist = INT_MAX;
            
            for (int j = 0; j < numUR; j++) {
                if (visited[j]) continue;
                int d = (curLoc == 0) ? 0 : graph->getDistance(curLoc, uRests[j]->location);
                if (d < minDist) {
                    minDist = d;
                    nearIdx = j;
                }
            }
            
            if (nearIdx == -1) break;
            
            Restaurant* rest = uRests[nearIdx];
            
            if (curLoc != 0) {
                int* path = new int[MAX_NODES];
                int plen;
                graph->getPath(curLoc, rest->location, path, plen);
                
                for (int j = 1; j < plen; j++) {
                    routes[rid][routeLens[rid]].location = path[j];
                    if (path[j] == rest->location) {
                        strcpy(routes[rid][routeLens[rid]].name, rest->name);
                        routes[rid][routeLens[rid]].isNamed = true;
                    } else {
                        routes[rid][routeLens[rid]].isNamed = false;
                    }
                    routeLens[rid]++;
                }
                routeTimes[rid] += minDist;
                delete[] path;
            } else {
                routes[rid][routeLens[rid]].location = rest->location;
                strcpy(routes[rid][routeLens[rid]].name, rest->name);
                routes[rid][routeLens[rid]].isNamed = true;
                routeLens[rid]++;
            }
            
            curLoc = rest->location;
            visited[nearIdx] = true;
            
            bool deliv[MAX_ORD] = {false};
            int nOrds = rOrdCnts[nearIdx];
            
            for (int j = 0; j < nOrds; j++) {
                int nearOrd = -1;
                int minODist = INT_MAX;
                
                for (int k = 0; k < nOrds; k++) {
                    if (deliv[k]) continue;
                    int d = graph->getDistance(curLoc, rOrds[nearIdx][k]->location);
                    if (d < minODist) {
                        minODist = d;
                        nearOrd = k;
                    }
                }
                
                if (nearOrd == -1) break;
                
                Order* ord = rOrds[nearIdx][nearOrd];
                
                int* path = new int[MAX_NODES];
                int plen;
                graph->getPath(curLoc, ord->location, path, plen);
                
                for (int k = 1; k < plen; k++) {
                    routes[rid][routeLens[rid]].location = path[k];
                    if (path[k] == ord->location) {
                        strcpy(routes[rid][routeLens[rid]].name, ord->name);
                        routes[rid][routeLens[rid]].isNamed = true;
                    } else {
                        routes[rid][routeLens[rid]].isNamed = false;
                    }
                    routeLens[rid]++;
                }
                
                routeTimes[rid] += minODist;
                curLoc = ord->location;
                deliv[nearOrd] = true;
                delete[] path;
            }
        }
    }
    
    void printRoutes() {
        for (int i = 0; i < numRiders; i++) {
            if (routeLens[i] > 0) {
                cout << "Rider " << (i + 1) << ": ";
                
                for (int j = 0; j < routeLens[i]; j++) {
                    cout << routes[i][j].location;
                    if (routes[i][j].isNamed) {
                        cout << " (" << routes[i][j].name << ")";
                    }
                    if (j < routeLens[i] - 1) {
                        cout << " -> ";
                    }
                }
                
                cout << " = " << routeTimes[i] << " time units" << endl;
            }
        }
        
        int total = 0;
        for (int i = 0; i < numRiders; i++) {
            total += routeTimes[i];
        }
        cout << "Total: " << total << " time units" << endl;
    }
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }
    
    ifstream infile(argv[1]);
    if (!infile) {
        cout << "Error: Cannot open file '" << argv[1] << "'" << endl;
        return 1;
    }
    
    cout << "============================================================" << endl;
    cout << "    Food Polar Bear - Delivery Route Optimization System    " << endl;
    cout << "============================================================" << endl;
    cout << "\nReading input from: " << argv[1] << "\n" << endl;
    
    int numTC;
    infile >> numTC;
    
    for (int tc = 1; tc <= numTC; tc++) {
        int gridSz, numRid, numRest;
        infile >> gridSz >> numRid >> numRest;
        
        cout << "\n============================================================" << endl;
        cout << "Test Case " << tc << endl;
        cout << "============================================================" << endl;
        cout << "Grid Size: " << gridSz << "x" << gridSz << endl;
        cout << "Number of Riders: " << numRid << endl;
        cout << "Number of Restaurants: " << numRest << endl;
        
        GridGraph graph(gridSz);
        Restaurant* rests = new Restaurant[numRest];
        
        int totOrds = 0;
        for (int i = 0; i < numRest; i++) {
            infile >> rests[i].name >> rests[i].location >> rests[i].orderCount;
            totOrds += rests[i].orderCount;
            
            for (int j = 0; j < rests[i].orderCount; j++) {
                infile >> rests[i].orders[j].name
                       >> rests[i].orders[j].location
                       >> rests[i].orders[j].timeLimit;
                rests[i].orders[j].assigned = false;
            }
        }
        
        cout << "Total Orders: " << totOrds << "\n" << endl;
        
        for (int i = 0; i < numRest; i++) {
            cout << "  " << rests[i].name << " (Location: " << rests[i].location << ")" << endl;
            for (int j = 0; j < rests[i].orderCount; j++) {
                cout << "    - " << rests[i].orders[j].name
                     << ": Location " << rests[i].orders[j].location
                     << ", Time Limit: " << rests[i].orders[j].timeLimit << endl;
            }
        }
        
        cout << "\n------------------------------------------------------------" << endl;
        cout << "Optimized Routes:" << endl;
        cout << "------------------------------------------------------------" << endl;
        
        RouteOptimizer opt(&graph, rests, numRest, numRid);
        opt.optimize();
        opt.printRoutes();
        
        delete[] rests;
        cout << endl;
    }
    
    infile.close();
    return 0;
}