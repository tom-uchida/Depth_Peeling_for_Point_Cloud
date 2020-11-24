#include <iostream>
#include <kvs/MersenneTwister>
#include <kvs/Vector3>
#include <kvs/BoxMuller>
#include <fstream>

#include <kvs/ColorMap>
#include <kvs/RGBColor>

const int num_of_points = 1e7;
const float TRUTH_MAX   = 0.99;
const float TRUTH_MIN   = 0.01;

const char OUTPUT_SPBR[] = "depth-box.spbr";

int main() {

    // FILE open
    std::ofstream fout;
    fout.open( OUTPUT_SPBR );

    // SPBR header setting
    fout << "#/SPBR_ASCII_Data"             << std::endl;
    fout << "#/RepeatLevel 1"               << std::endl;
    fout << "#/BGColorRGBByte 255 255 255"  << std::endl;
    fout << "#/ImageResolution 1000"        << std::endl;
    fout << "#/LOD 0"                       << std::endl;
    fout << "#/Shading 0"                   << std::endl;
    fout << "#/EndHeader"                   << std::endl;

    // Set depth
    const size_t depth = 5;

    // Set color map
    auto cmap = kvs::ColorMap::Viridis( 256 );
    cmap.setRange( 0, depth );

    // Set Bounding-Box
    const kvs::Vector3f BB_max( 2, 2, depth );
    const kvs::Vector3f BB_min( 0, 0,     0 );
    const float BB_x = BB_max.x() - BB_min.x();
    const float BB_y = BB_max.y() - BB_min.y();
    const float BB_z = BB_max.z() - BB_min.z();

    // Generate points
    kvs::MersenneTwister  uniRand;
    // kvs::BoxMuller        normRand;
    kvs::RGBColor color;
    float x, y, z;
    for ( int i = 0; i < num_of_points; i++ ) {
        // Generate random 3D point in the BB
        x = BB_x*uniRand() + BB_min.x(); // x coord is a random number [BB_min.x, BB_min.x]
        y = BB_y*uniRand() + BB_min.y(); // y coord is a random number [BB_min.y, BB_min.y]
        z = BB_z*uniRand() + BB_min.z(); // z coord is a random number [BB_min.z, BB_min.z]

        color = cmap.at( depth - z );
        fout << x << " " << y << " " << z << " ";
        fout << 0 << " " << 0 << " " << 0 << " ";
        fout << +color.r() << " " << +color.g() << " " << +color.b() << std::endl;
    } // end for

    // FILE close
    fout.close();

    return 0;
}