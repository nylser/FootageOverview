/*
 * convert weird *.264 file to mp4 and wav
 * -raspo666 2018
 */

#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>


#ifndef bzero
#define bzero(b,len) (memset((b), '\0', (len)), (void) 0)
#endif // bzero
#ifndef bcopy
#define bcopy(b1,b2,len) (memmove((b2), (b1), (len)), (void) 0)
#endif // bcopy

/*WAV*/


typedef struct wav_header
{
    // RIFF Header
    char riff_header[4]; // Contains "RIFF"
    int wav_size; // Size of the wav portion of the file, which follows the first 8 bytes. File size - 8
    char wave_header[4]; // Contains "WAVE"

    // Format Header
    char fmt_header[4]; // Contains "fmt " (includes trailing space)
    int fmt_chunk_size; // Should be 16 for PCM
    short audio_format; // Should be 1 for PCM. 3 for IEEE Float
    short num_channels;
    int sample_rate;
    int byte_rate; // Number of bytes per second. sample_rate * num_channels * Bytes Per Sample
    short sample_alignment; // num_channels * Bytes Per Sample
    short bit_depth; // Number of bits per sample

    // Data
    char data_header[4]; // Contains "data"
    int data_bytes; // Number of bytes in data. Number of samples * num_channels * sample byte size
    // uint8_t bytes[]; // Remainder of wave file is bytes
} wav_header;








int main(int ac, char **av)
{
    FILE *in,*out,*outa;
    wav_header ahead;

    char *buffer,*p,ccode[5],*strbuf,*strp;
    int count,bufsiz,abytes;
    int len = 0;

    if(ac != 2)
        exit(printf("use %s <file> \n",av[0]));

    if(!(in = fopen(av[1],"rb")))
        exit(printf("cannot open %s for reading.\n",av[1]));

    /* try to allocate a buffer size of infile */
    fseek(in,0,SEEK_END);
    bufsiz = ftell(in);
    rewind(in);
    if(!(buffer = malloc(bufsiz)))
        exit(printf("unable to allocate %d bytes\n",bufsiz));
    p = buffer;
    /* open output */


    if(!(strbuf = malloc(strlen(av[1])+5)))
        exit(printf("no mem for strings\n"));


    strp = strstr(av[1],".264");
    if(strp != NULL)
        *strp = '\0';
    strp = av[1];


    sprintf(strbuf,"%s_pre.mp4",strp);

    if(!(out = fopen(strbuf,"wb")))
        exit(printf("cannot open %s for writing.\n",av[2]));

    sprintf(strbuf,"%s_pre.wav",strp);

    if(!(outa = fopen(strbuf,"wb")))
        exit(printf("cannot open %s for writing.\n",strbuf));

    fwrite(&ahead,sizeof(wav_header),1,outa);
    /* get data */
    count = fread(buffer,1,bufsiz,in);
    abytes = 0;
    if(count != bufsiz)
    {
        printf("could only read %d of %d bytes\n",count,bufsiz);
        exit(0);
    }
    /* Throw first 0x10 bytes of garbage/fileheader plus first videoheader */
    p += 0x10;

    while(p-buffer < bufsiz)
    {
        bzero(ccode,5);
        bcopy(p,ccode,4);
        p += 4;
        bcopy(p,&len,4);
        if(!(strncmp((char *)ccode,"HXAF",4)))
        {
            p += 0xc;
            p += 4; // {0x0001, 0x5000} whatever that means, it must go, it's no audio
            len -= 4;
            printf("code: HXAF audio  %d bytes\n",len);
            fwrite(p,1,len,outa);
            p += len;
            abytes += len;
            continue;
        }
        else if(!(strncmp((char *)ccode,"HXFI",4)))
        {
            printf("found code HXFI, exit\n");
            break; /* some sort of table follows */
        }
        /* this will break if there's some other ccode ! */
        printf("code: %s video %d bytes\n",ccode,len);
        p += 0xc;
        fwrite(p,1,len,out);
        p += len;
    }

    /* wav header */

    strncpy(ahead.riff_header,"RIFF",4);
    strncpy(ahead.wave_header,"WAVE",4);
    strncpy(ahead.fmt_header,"fmt ",4);
    strncpy(ahead.data_header,"data",4);

    ahead.fmt_chunk_size = 16;
    ahead.audio_format = 0x6;
    ahead.num_channels = 1;
    ahead.sample_rate = 8000;
    ahead.byte_rate = 8000; // 16 ??
    ahead.sample_alignment = 2;
    ahead.bit_depth = 16;
    ahead.data_bytes = abytes;
    ahead.wav_size = abytes + sizeof(wav_header) - 8;
    fseek(outa,0,SEEK_SET);
    fwrite(&ahead,sizeof(wav_header),1,outa);

    free(buffer);
    fclose(in);
    fclose(out);
    fclose(outa);
    exit(0);

}

