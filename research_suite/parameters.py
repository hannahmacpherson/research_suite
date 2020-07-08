


number_of_extra_bps_upstream = 50
number_of_extra_bps_downstream = 10


# this was created with HLA in mind, so many sequences won't fit a certain primer because they're so polymorphic. 
# Since the idea is to cut the sequence xbp upstream and downstream anyway so you can design primers, slight length variations won't matter.
# if you can find published primers, these work great, but you could just use the start/end of the known HLA sequence and then the preceeding/following 300bp for example. 
# it will try options 1 by 1. If you only want to try one option just fill in the same sequence for each one
forward_primer_option1 = 'GGGGAGGGCAAAGTCCC' 
forward_primer_option2 = 'GTGGCTCTCAAGGGCTCAG'
forward_primer_option3 = 'GCACAGGAGGGGGA'


reverse_primer_complement_option1 = 'TCGAACATATGCC' 
reverse_primer_complement_option2 = 'AATGTCACAA'
reverse_primer_complement_option3 = 'TCTCCATCAGACTGAATCAG' 