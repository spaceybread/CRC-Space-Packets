use std::fs::File;
use std::fs;
use std::env;

fn table() -> [u32; 256] {
    let mut table = [0; 256];
    for i in 0..256 {
        table[i as usize] = (0..8).fold(i as u32, |acc, _| {
            match acc & 1 {
                1 => 0xedb88320 ^ (acc >> 1),
                _ => acc >> 1
            }
        });
    }
    return table;
}

fn hash(buf: &str, table: [u32; 256]) -> u32 {
    !buf.bytes().fold(!0, |acc, octet| {
        (acc >> 8) ^ table[((acc & 0xff) ^ octet as u32) as usize]
    })
}

fn readFile() -> Vec<u8> {
    let contents: Vec<u8> = fs::read("packetWithouCS").expect("File read failure!");
    println!("File read!");
    return contents;
}


fn main() {
    let r = readFile();

    let table = table();
    //println!("{:x}", hash(&r, table));
}