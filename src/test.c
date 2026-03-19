#include <stdio.h>
#include <stdlib.h>
#include "kd.h"
#include "voronoi.h"

int main() 
{

    point_t pts[] = 
    {
        {1.0, 1.0, 0},
        {4.0, 4.0, 1},
        {7.0, 2.0, 2},
        {2.0, 8.0, 3}
    };

    kdnode_t *root = kd_build(pts, 4);

    point_t query = {3.9, 4.1, -1};

    // ── Task 2 test: nearest neighbor ──
    point_t result = kd_nearest(root, query);
    printf("nearest to (3.9, 4.1) -> id=%d  x=%.1f  y=%.1f\n",
            result.id, result.x, result.y);

    // ── Task 3 test: k-NN ──
    int count = 0;
    point_t *neighbors = kd_knn(root, query, 3, &count);

    printf("3 nearest to (3.9, 4.1):\n");
    for (int i = 0; i < count; i++) {
        printf("  [%d] id=%d  x=%.1f  y=%.1f\n",
                i, neighbors[i].id, neighbors[i].x, neighbors[i].y);
    }
    free(neighbors);

    // ── Task 4 test: voronoi_build ──
    dcel_t *dcel = voronoi_build(pts, 4);
    printf("voronoi_build output: %d vertices, %d edges, %d faces\n", dcel->nv, dcel->ne, dcel->nf);
    
    int nbr_count = 0;
    face_t** nbrs = dcel_neighbours(dcel, 0, &nbr_count);
    printf("dcel_neighbours for site 0: %d neighbours\n", nbr_count);
    free(nbrs);
    voronoi_free(dcel);

    kd_free(root);
    return 0;
}


/*compile and run:
gcc -std=c11 -o test_run kd.c test.c -lm
./test_run
*/