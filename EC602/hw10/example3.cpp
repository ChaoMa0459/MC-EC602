// Copyright 2016 Alejandro Alex Jingwei Michael
#include <stdlib.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#define ALPHABETS 26
using std::string;
using std::map;
using std::vector;

struct node {
 public:
    char me;
    struct node *parent;
    struct node *children[ALPHABETS];
    string word = "";
    bool ep = false;        // Endpoint?
};
struct puzzle {
 public:
    int dimension = 0;
    vector< vector<char> > board;
    void clear_board(int d);
    void display(int n);
};

int solve_controller(puzzle *puz,
        node *trie,
        vector<int> lengths,
        map<int, char> sol,
        vector<string> *words,
        std::set<string> *solset);
node * root;
void puzzle::clear_board(int d) {
    dimension = d;
    board.clear();
    board.resize(dimension, vector<char>(d, 0));
}


bool load_puzzle(string js, std::vector<int> *lengths,  puzzle *puz) {
    std::size_t lb = js.find('[');
    std::size_t rb = js.find(']');
    std::string words = js.substr(lb+1, rb-lb-1);
    lb = js.find('[', rb+1);
    rb = js.find(']', rb+1);
    std::string len = js.substr(lb+1, rb-lb-1);
    int i = 0;
    while (1) {
        std::size_t lq = words.find('"');
        if (lq == std::string::npos)
            break;
        std::size_t rq = words.find('"', lq+1);
        std::string word = words.substr(lq+1, rq-lq-1);
        words.erase(lq, rq-lq+1);
        if (word.length() != puz->dimension)
            puz->clear_board(word.length());
        for (int j=0; j< puz->dimension; j++)
            puz->board[i][j] = word[puz->dimension-1-j];
        i++;
    }
    while (len.length()) {
        std::size_t rc = words.find(',');
        if (rc == std::string::npos)
            break;
        int num = std::stoi(len.substr(0, rc-1));
        lengths->push_back(num);
        len.erase(0, 2);
    }
    if (lengths->size() ==0 || puz->dimension ==0)
        return false;
    return true;
}
int solve_puzzle(puzzle *puz,
        vector<int> lengths,
        node *trie,
        map< int, char > *sol,
        int cellx, int celly,
        vector<string> *words,
        std::set<string> *solset
        ) {
    if (!trie)return false;
    map< int, char > tsol;
    tsol.insert(sol->begin(), sol->end());
    (tsol)[cellx+celly*puz->dimension] = trie->me;
    for (const auto &p : (*sol))
        if (trie->ep) {
            vector<int> tlengths = lengths;
            tlengths.erase(tlengths.begin());
            vector<string> twords = *words;
            twords.push_back(trie->word);
            for (const auto &p : (twords))
                if (solve_controller(puz, root, tlengths,
                                     tsol, &twords, solset)) {
                    *words = twords;
                    *sol = tsol;
                    return true;
                } else {
                    return false;
                }
        }
    int minx =  (cellx -1 > 0) ? cellx -1: 0;
    int miny =  (celly -1 > 0) ? celly -1: 0;
    int maxx =  (cellx +1 < puz->dimension) ? cellx +1: puz->dimension-1;
    int maxy =  (celly +1 < puz->dimension) ? celly +1: puz->dimension-1;
    for (int x = minx; x <= maxx; x++) {
        for (int y = miny; y <= maxy; y++) {
            if (tsol.count(x+y*puz->dimension))
                continue;
            char c;
            try {
                c = puz->board.at(x).at(y);
            }
            catch(std::out_of_range) {
                continue;
            }
            if (trie->children[c-'a']) {
                if (solve_puzzle(puz, lengths,
                                 trie->children[puz->board.at(x).at(y)-'a'] , &
                                 tsol, x, y, words, solset)) {
                    sol->insert(tsol.begin(), tsol.end());
                    return true;
                }
            }
        }
    }
    return false;
}

int solve_controller(puzzle *puz,
        node *trie,
        vector<int> lengths,
        map<int, char> sol,
        vector<string> *words,
        std::set<string> *solset) {
    if (lengths.size() == 0) {
        string sols = "";
        for (const auto &p : *words)
            sols+= p +" ";
        solset->insert(sols);
        return false;
    }
    puzzle tpuz = *puz;
    for (std::map<int, char>::reverse_iterator it=sol.rbegin();
            it != sol.rend(); ++it) {
        tpuz.board[it->first%tpuz.dimension].erase(
                tpuz.board[it->first%tpuz.dimension].begin()
                + it->first/tpuz.dimension);
    }
    for (int x = 0; x < tpuz.board.size(); x++) {
        for (int y = 0; y < tpuz.board.at(x).size(); y++) {
            map< int, char > tsol;
            vector<string> twords = *words;
            if (solve_puzzle(&tpuz, lengths,
                        trie->children[lengths.front()]->children[tpuz.
                        board.at(x).at(y)-'a'], &tsol, x, y, &twords, solset)) {
                *words = twords;
                return true;
            }
        }
    }
    return false;
}

int load_dictionary(string fn, node *trie) {
    ifstream infile(fn);
    string s;
    int count;
    while ( infile >> s ) {
        if (s.length() > ALPHABETS)
            continue;
        count++;
        if (trie->children[s.length()] == NULL) {
            trie->children[s.length()] = new node;
            trie->children[s.length()]->parent = trie;
            trie->children[s.length()]->me = '0' + s.length();
        }
        node * traverse = trie->children[s.length()];
        for (auto c : s) {
            if (traverse->children[c-'a'] == NULL) {
                traverse->children[c-'a'] = new node;
                traverse->children[c-'a']->parent = traverse;
                traverse->children[c-'a']->me = c;
            }
            traverse = traverse->children[c-'a'];
        }
        traverse->ep = true;
        traverse->word = s;
    }
    return count;
}

int main() {
    puzzle puz = puzzle();
    std::string json;
    node trie = node();
    node ltrie = node();
    load_dictionary("small_word_list.txt", &trie);
    load_dictionary("large_word_list.txt", &ltrie);
    while (getline(cin, json)) {
        root = &trie;
        map< int, char > sol;
        vector<int> lengths;
        if (!load_puzzle(json, &lengths, &puz))
            return false;
        vector<string> words;
        std::set<string> solset;
        solve_controller(&puz, &trie, lengths, sol, &words, &solset);
        if (solset.size() == 0) {
            root = &ltrie;
            solve_controller(&puz, &ltrie, lengths, sol, &words, &solset);
        }
        for (const auto &p : solset) {
            cout << p <<endl;
        }
        cout << "." << endl;
    }
}
