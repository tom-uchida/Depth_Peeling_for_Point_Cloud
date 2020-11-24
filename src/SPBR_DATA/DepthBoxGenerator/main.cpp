// 平面の点群を人工的に生成するプログラム

#include <iostream>
#include <kvs/MersenneTwister>
#include <kvs/Vector3>
#include <kvs/BoxMuller>
#include <fstream>

#include <kvs/ColorMap>
#include <kvs/RGBColor>

const int npoints = 10000000;
#define  TRUTH_MAX    0.99
#define  TRUTH_MIN    0.01

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
    kvs::BoxMuller        normRand;
    kvs::RGBColor color;
    float x, y, z;
    for ( int i = 0; i < npoints; i++ ) {
        // Generate random 3D point in the BB
        x = BB_x*uniRand() + BB_min.x(); // x coord is a random number [BB_min.x, BB_min.x]
        y = BB_y*uniRand() + BB_min.y(); // y coord is a random number [BB_min.y, BB_min.y]
        z = BB_z*uniRand() + BB_min.z(); // z coord is a random number [BB_min.z, BB_min.z]

        color = cmap.at( depth - z );
        fout << x << " " << y << " " << z << " ";
        fout << 0 << " " << 0 << " " << 0 << " ";
        fout << +color.r() << " " << +color.g() << " " << +color.b() << std::endl;
        // fout << 255 << " " << 255 << " " << 255 << std::endl;

        // if ( i < 10 ) {
        //     std::cout << "R: " << color.r() << std::endl;
        //     std::cout << "G: " << color.g() << std::endl;
        //     std::cout << "B: " << color.b() << std::endl;
        // }
    }

    // FILE close
    fout.close();

    return 0;
}